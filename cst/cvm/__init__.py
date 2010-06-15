#!/usr/bin/env python
"""
SCEC Community Velocity Model
"""
import os, sys, re, shutil, urllib, tarfile
import cst.util
import cst.conf
from cst.conf import launch

path = os.path.dirname( os.path.realpath( __file__ ) )
url = 'http://www.data.scec.org/3Dvelocity/Version4.tar.gz'
url = 'http://earth.usc.edu/~gely/coseis/download/cvm4.tgz'

def _build( mode=None, optimize=None ):
    """
    Build CVM code.
    """

    # configure
    cf = cst.conf.configure( 'cvm' )[0]
    if not optimize:
        optimize = cf.optimize
    if not mode:
        mode = cf.mode
    if not mode:
        mode = 'asm'

    # download model
    tarball = os.path.join( cf.repo, os.path.basename( url ) )
    if not os.path.exists( tarball ):
        if not os.path.exists( cf.repo ):
            os.makedirs( cf.repo )
        print( 'Downloading %s' % url )
        urllib.urlretrieve( url, tarball )

    # build directory
    cwd = os.getcwd()
    os.chdir( path )
    if not os.path.exists( 'build' ):
        os.makedirs( 'build' )
        fh = tarfile.open( tarball, 'r:gz' )
        fh.extractall( 'build' )
        if os.system( 'patch -p0 < cvm4.patch' ):
            sys.exit( 'Error patching CVM' )
    os.chdir( 'build' )

    # find array sizes, save it for later
    for line in file( 'in.h', 'r' ).readlines():
        if line[0] != ' ':
            continue
        pat = re.compile( 'ibig *= *([0-9]*)' ).search( line )
        if pat:
            ibig = pat.groups()[0]
    open( 'ibig', 'w' ).write( str( ibig ) )

    # compile ascii, binary, and MPI versions
    if 'a' in mode:
        source = 'iotxt.f', 'version4.0.f'
        for opt in optimize:
            compiler = cf.fortran_serial + cf.fortran_flags[opt] + ('-o',)
            object_ = 'cvm4-a' + opt
            cst.conf.make( compiler, object_, source )
    if 's' in mode:
        source = 'iobin.f', 'version4.0.f'
        for opt in optimize:
            compiler = cf.fortran_serial + cf.fortran_flags[opt] + ('-o',)
            object_ = 'cvm4-s' + opt
            cst.conf.make( compiler, object_, source )
    if 'm' in mode and cf.fortran_mpi:
        source = 'iompi.f', 'version4.0.f'
        for opt in optimize:
            object_ = 'cvm4-m' + opt
            compiler = cf.fortran_mpi + cf.fortran_flags[opt] + ('-o',)
            cst.conf.make( compiler, object_, source )
    os.chdir( cwd )
    return

def stage( inputs={}, **kwargs ):
    """
    Stage job
    """

    print( 'CVM setup' )

    # update inputs
    inputs = inputs.copy()
    inputs.update( kwargs )

    # configure
    job, inputs = cst.conf.configure( module='cvm', **inputs )
    if inputs:
        sys.exit( 'Unknown parameter: %s' % inputs )
    if not job.mode:
        job.mode = 's'
        if job.nproc > 1:
            job.mode = 'm'
    job.command = os.path.join( '.', 'cvm4' + '-' + job.mode + job.optimize )
    job = cst.conf.prepare( job )

    # check minimum processors needed for compiled memory size
    f = os.path.join( path, 'build', 'ibig' )
    ibig = int( open( f, 'r' ).read() )
    minproc = int( job.nsample / ibig )
    if job.nsample % ibig != 0:
        minproc += 1
    if minproc > job.nproc:
        sys.exit( 'Need at lease %s processors for this mesh size' % minproc )

    # create run directory
    if job.force == True and os.path.isdir( job.rundir ):
        shutil.rmtree( job.rundir )
    if not job.reuse or not os.path.exists( job.rundir ):
        f = os.path.join( path, 'build' )
        shutil.copytree( f, job.rundir )
    else:
        for f in (
            job.lon_file, job.lat_file, job.dep_file,
            job.rho_file, job.vp_file, job.vs_file
        ):
            ff = os.path.join( job.rundir, f )
            if os.path.exists( ff ):
                os.remove( ff )

    # save configuration
    f = os.path.join( job.rundir, 'conf.py' )
    cst.util.save( f, job.__dict__ )

    return job

