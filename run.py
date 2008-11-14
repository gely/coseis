#!/usr/bin/env python
"""
SORD main module
"""

import os, sys, pwd, glob, time, getopt, shutil
import util, setup, configure, fieldnames
callcount = 0

def run( params ):
    """Setup, and optionally launch, a SORD job"""

    global callcount
    callcount += 1

    # Save start time
    starttime = time.asctime()
    print "SORD setup"

    # Command line options
    prepare = True
    run = False
    mode = None
    optimize = 'O'
    opts, machine = getopt.getopt( sys.argv[1:], 'niqsmgGtpOd' )
    for o, v in opts:
        if   o == '-n': prepare = False; run = False
        elif o == '-i': run = 'i'
        elif o == '-q': run = 'q'
        elif o == '-s': mode = 's'
        elif o == '-m': mode = 'm'
        elif o == '-g': optimize = 'g'
        elif o == '-G': optimize = 'g'; run = 'g'
        elif o == '-t': optimize = 't'
        elif o == '-p': optimize = 'p'
        elif o == '-O': optimize = 'O'
        elif o == '-d':
            if callcount is 1:
                f = 'run' + os.sep + '[0-9][0-9]'
                for f in glob.glob( f ): shutil.rmtree( f )
        else: sys.exit( 'Error: unknown option: %s %s' % ( o, v ) )

    # Configure machine
    if machine: machine = machine[0]
    cfg = util.objectify( configure.configure( machine ) )
    print 'Machine: ' + cfg.machine

    # Prep parameters 
    params = prepare_params( params )

    # Number of processors
    np3 = params.np[:]
    totalcores = cfg.nodes * cfg.cores
    if not mode and totalcores == 1: mode = 's'
    if mode == 's': np3 = [ 1, 1, 1 ]
    np = np3[0] * np3[1] * np3[2]
    if not mode:
        mode = 's'
        if np > 1: mode = 'm'
    if cfg.cores:
        nodes = min( cfg.nodes, ( np - 1 ) / cfg.cores + 1 )
        ppn = ( np - 1 ) / nodes + 1
        cores = min( cfg.cores, ppn )
    else:
        nodes = 1
        ppn = np
        cores = np

    # Domain size
    nm3 = [ ( params.nn[i] - 1 ) / np3[i] + 3 for i in range(3) ]
    i = params.faultnormal - 1
    if i >= 0: nm3[i] = nm3[i] + 2
    nm = nm3[0] * nm3[1] * nm3[2]

    # RAM and Wall time usage
    floatsize = 4
    if params.oplevel in (1,2): nvars = 20
    elif params.oplevel in (3,4,5): nvars = 23
    else: nvars = 44
    ramcore = ( nm * nvars * floatsize / 1024 / 1024 + 10 ) * 1.5
    ramnode = ( nm * nvars * floatsize / 1024 / 1024 + 10 ) * ppn
    sus = ( params.nt + 10 ) * ppn * nm / cores / cfg.rate / 3600000 * nodes * cfg.cores
    mm  = ( params.nt + 10 ) * ppn * nm / cores / cfg.rate / 60000 * 1.5 + 10
    if cfg.timelimit: mm = min( 60*cfg.timelimit[0] + cfg.timelimit[1], mm )
    hh = mm / 60
    mm = mm % 60
    walltime = '%d:%02d:00' % ( hh, mm )
    print 'Cores: %s of %s' % ( np, totalcores )
    print 'Nodes: %s of %s' % ( nodes, cfg.nodes )
    print 'RAM: %sMb of %sMb per node' % ( ramnode, cfg.ram )
    print 'Time limit: ' + walltime
    print 'SUs: %s' % sus
    if cfg.cores and ppn > cfg.cores:
        print 'Warning: exceding available cores per node (%s)' % cfg.cores
    if cfg.ram and ramnode > cfg.ram:
        print 'Warning: exceding available RAM per node (%sMb)' % cfg.ram

    # Set-up and run
    if not prepare: return

    # Compile code
    setup.build( mode, optimize )

    # Create run directory
    try: os.mkdir( 'run' )
    except: pass
    count = glob.glob( 'run' + os.sep + '[0-9][0-9]' )
    try: count = count[-1].split( os.sep )[-1]
    except: count = 0
    count = '%02d' % ( int( count ) + 1 )
    rundir = 'run' + os.sep + str( count )
    print 'Run directory: ' + rundir
    rundir = os.path.realpath( rundir )
    os.mkdir( rundir )
    for f in ( 'in', 'out', 'prof', 'stats', 'debug', 'checkpoint' ):
        os.mkdir( rundir + os.sep + f )

    # Link input files
    for i, line in enumerate( params.fieldio ):
        if 'r' in line[0] and os.sep in line[3]:
            filename = line[3]
            f = os.path.basename( filename )
            line = line[:3] + ( f, ) + line[4:]
            params.fieldio[i] = line
            f = 'in' + os.sep + filename
            try:
                os.link( filename, rundir + os.sep + f )
            except:
                shutil.copy( filename, rundir + os.sep + f )

    # Template variables
    code = 'sord'
    pre = ''
    bin = './sord-' + mode + optimize
    post = ''
    os_ = os.uname()[3]
    host = os.uname()[1]
    user = pwd.getpwuid(os.geteuid())[0]
    #user = os.getlogin()
    rundate = time.asctime()
    machine = cfg.machine

    # Email address
    cwd = os.path.realpath( os.getcwd() )
    os.chdir( os.path.realpath( os.path.dirname( __file__ ) ) )
    if os.path.isfile( 'email' ):
        email = file( 'email', 'r' ).read().strip()
    else:
        #email = os.getlogin()
        email = pwd.getpwuid(os.geteuid())[0]
        file( 'email', 'w' ).write( email )

    # Copy files to run directory
    files = [ 'sord.tgz', 'bin' + os.sep + 'sord-' + mode + optimize ]
    if optimize == 'g':
        files += glob.glob( 'src/*.f90' )
    for f in files:
        f = f.replace( '/', os.sep )
        shutil.copy( f, rundir )
    for d in cfg.templates:
        for f in glob.glob( d + os.sep + '*' ):
            ff = rundir + os.sep + os.path.basename( f )
            out = file( f, 'r' ).read() % locals()
            file( ff, 'w' ).write( out )
            shutil.copymode( f, ff )

    # Write parameter file
    os.chdir( rundir )
    log = file( 'log', 'w' )
    log.write( starttime + ': SORD setup started\n' )
    write_params( params )

    # Run or que job
    if run == 'q':
        print 'que.sh'
        if os.uname()[1] not in cfg.hosts:
            sys.exit( 'Error: hostname %r does not match configuration %r' % ( host, machine ) )
        #if subprocess.call( '.' + os.sep + 'que.sh' ):
        if os.system( '.' + os.sep + 'que.sh' ):
            sys.exit( 'Error queing job' )
    elif run:
        print 'run.sh -' + run
        if os.uname()[1] not in cfg.hosts:
            sys.exit( 'Error: hostname %r does not match configuration %r' % ( host, machine ) )
        #if subprocess.call( [ '.' + os.sep + 'run.sh', '-' + run ] ):
        if os.system( '.' + os.sep + 'run.sh -' + run ):
            sys.exit( 'Error running job' )

    # Return to initial directory
    os.chdir( cwd )

def prepare_params( pp ):
    """Prepare input paramers"""

    itbuff = 10 # XXX should this go in a settings file?

    # merge input parameters with defaults
    f = os.path.dirname( __file__ ) + os.sep + 'defaults.py'
    p = util.load( f )
    for k, v in pp.iteritems():
        if k is 'fieldio':
            p['fieldio'] += pp['fieldio']
        elif k[0] is not '_' and type(v) is not type(sys):
            if k not in p:
                sys.exit( 'Unknown SORD parameter: %s = %r' % ( k, v ) )
            p[k] = v
    p = util.objectify( p )

    # hypocenter node
    ii = list( p.ihypo )
    for i in range( 3 ):
        if ii[i] < 1:
            ii[i] = ii[i] + p.nn[i] + 1
    p.ihypo = tuple( ii )

    # boundary conditions
    i1 = list( p.bc1 )
    i2 = list( p.bc2 )
    i = abs( p.faultnormal ) - 1
    if i >= 0:
        if p.ihypo[i] >= p.nn[i]: sys.exit( 'Error: ihypo %s out of bounds' % ii )
        if p.ihypo[i] == p.nn[i] - 1: i1[i] = -2
        if p.ihypo[i] == 1:           i2[i] = -2
    p.bc1 = tuple( i1 )
    p.bc2 = tuple( i2 )

    # PML region
    i1 = [ 0, 0, 0 ]
    i2 = [ n+1 for n in p.nn ]
    if p.npml > 0:
        for i in range( 3 ):
            if p.bc1[i] == 10: i1[i] = p.npml
            if p.bc2[i] == 10: i2[i] = p.nn[i] - p.npml + 1
            if i1[i] > i2[i]: sys.exit( 'Error: model too small for PML' )
    p.i1pml = tuple( i1 )
    p.i2pml = tuple( i2 )

    # I/O sequence
    fieldio = []
    for line in p.fieldio:
        line = list( line )
        filename = '-'
        x1 = x2 = 0., 0., 0.
        tfunc, val, period = 'const', 1.0, 1.0
        op = line[0][0]
        mode = line[0][1:]
        if op not in '=+': sys.exit( 'Error: unsupported operator: %r' % line )
        try:
            if   mode == '':    f, ii, val                        = line[1:]
            elif mode == 's':   f, ii, val                        = line[1:]
            elif mode == 'x':   f, ii, val, x1                    = line[1:]
            elif mode == 'sx':  f, ii, val, x1                    = line[1:]
            elif mode == 'c':   f, ii, val, x1, x2                = line[1:]
            elif mode == 'f':   f, ii, val, tfunc, period         = line[1:]
            elif mode == 'fs':  f, ii, val, tfunc, period         = line[1:]
            elif mode == 'fx':  f, ii, val, tfunc, period, x1     = line[1:]
            elif mode == 'fsx': f, ii, val, tfunc, period, x1     = line[1:]
            elif mode == 'fc':  f, ii, val, tfunc, period, x1, x2 = line[1:]
            elif mode == 'r':   f, ii, filename                   = line[1:]
            elif mode == 'w':   f, ii, filename                   = line[1:]
            elif mode == 'rx':  f, ii, filename, x1               = line[1:]
            elif mode == 'wx':  f, ii, filename, x1               = line[1:]
            else: sys.exit( 'Error: bad i/o mode: %r' % line )
        except:
            sys.exit( 'Error: bad i/o spec: %r' % line )
        mode = mode.replace( 'f', '' )
        if f not in fieldnames.all:
            sys.exit( 'Error: unknown field: %r' % line )
        if p.faultnormal == 0 and f in fieldnames.fault:
            sys.exit( 'Error: field only for ruptures: %r' % line )
        if 'w' not in mode and f not in fieldnames.input:
            sys.exit( 'Error: field is ouput only: %r' % line )
        if 'r' in mode:
            fn = os.path.dirname( filename ) + os.sep + 'endian'
            if file( fn, 'r' ).read()[0] != sys.byteorder[0]:
                sys.exit( 'Error: wrong byte order for ' + filename )
        if f in fieldnames.cell:
            mode = mode.replace( 'x', 'X' )
            mode = mode.replace( 'c', 'C' )
            nn = [ n-1 for n in p.nn ] + [ p.nt ]
        else:
            nn = list( p.nn ) + [ p.nt ]
        ii = util.indices( ii, nn )
        if f in fieldnames.initial:
            ii[3] = 0, 0, 1
        if f in fieldnames.fault:
            i = p.faultnormal - 1
            ii[i] = 2 * ( p.ihypo[i], ) + ( 1, )
        nn = [ ( ii[i][1] - ii[i][0] + 1 ) / ii[i][2] for i in range(4) ]
        nb = min( nn[3], min( p.itio, itbuff ) )
        n = nn[0] * nn[1] * nn[2]
        if n == 1:
            nb = p.itio
        elif n > ( p.nn[0] + p.nn[1] + p.nn[2] ) ** 2:
            nb = 1
        fieldio += [( op+mode, f, ii, filename, nb, val, tfunc, period, x1, x2 )]
    f = [ line[3] for line in fieldio if line[3] != '-' ]
    for i in range( len( f ) ):
        if f[i] in f[:i]:
            sys.exit( 'Error: duplicate filename: %r' % f[i] )
    p.fieldio = fieldio
    return p

def write_params( params, filename='parameters.py' ):
    """Write input file that will be read by SORD Fortran code"""
    f = file( filename, 'w' )
    f.write( '# Auto-generated SORD input file\n' )
    for k in dir( params ):
        v = getattr( params, k )
        if k[0] is not '_' and k is not 'fieldio' and type(v) is not type(os):
            f.write( '%s = %r\n' % ( k, v ) )
    f.write( 'fieldio = [\n' )
    for line in params.fieldio: f.write( repr( line ) + ',\n' )
    f.write( ']\n' )

