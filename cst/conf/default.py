"""
Coseis Default Configuration
"""

import os, sys, pwd, socket
import numpy as np

# email address
try:
    import configobj
    f = os.path.join(os.path.expanduser('~'), '.gitconfig')
    email = configobj.ConfigObj(f)['user']['email']
    del(configobj, f)
except:
    email = pwd.getpwuid(os.geteuid())[0]

# job parameters
code = 'cst'              # code name
name = 'cst'              # job name
verbose = False           # extra diagnostics
prepare = True            # True: setup run directory, False: dry run
run = ''                  # 'exec': interactive, 'submit': batch queue
rundir = 'run/{name}'     # name of the run directory
new = True                # create new run directory
force = False             # overwrite previous run directory
stagein = []              # files to copy into run directory
dtype = np.dtype('f').str # Numpy data type
nproc = 1                 # number of processes
nthread = 0               # number of threads per process
command = ''              # executable command
pre = post = ''           # pre and post-processing commands
depend = ''               # job ID to wait for
minutes = 0               # estimated run time

# machine specific
machine = ''
account = ''
host = socket.getfqdn()
host_opts = {}
system = os.uname()
queue = ''
queue_opts = []
ppn_range = []
maxnodes = 1
maxcores = 1
maxram = 0
pmem = 0
maxtime = 0
rate = 1.0e6
nstripe = -2

# command line options
argv = sys.argv[1:]
options = [
    ('v', 'verbose',     'verbose', True),
    ('f', 'force',       'force',   True),
    ('n', 'dry-run',     'prepare', False),
    ('i', 'interactive', 'run',     'exec'),
    ('q', 'queue',       'run',     'submit'),
]

# search for files in PATH
def find(*files):
    import os
    path = os.environ['PATH'].split(':')
    for f in files:
        for p in path:
            if os.path.isfile(os.path.join(p, f)):
                return f

# default compiler: GNU
f2py_flags = ''
build_cc  = find('mpicc', 'gcc')
build_fc = find('mpif90', 'gfortran') + ' -fimplicit-none'
build_ld  = find('mpif90', 'gfortran')
build_mpi = 'mpi' in build_ld
build_libs = ''
build_flags = '-g -O3 -Wall -fopenmp -fbounds-check -ffpe-trap=invalid,zero,overflow'
build_flags = '-g -O3 -Wall -fopenmp -fdefault-real-8'
build_flags = '-g -O3 -Wall -fopenmp -pg'
build_flags = '-g -O3 -Wall -fopenmp'

# default scheduler: PBS
if build_mpi:
    launch = 'mpiexec -np {nproc} {command}'
else:
    launch = '{command}'
notify_threshold = 4096
notify = '-m abe'
submit_flags = ''
submit_pattern = r'(?P<jobid>\d+\S*)\D*$'
submit = 'qsub {notify} {submit_flags} "{name}.sh"'
submit2 = 'qsub {notify} -W depend="afterok:{depend}" {submit_flags} "{name}.sh"'

# batch script
script = """\
#!/bin/sh
cd "{rundir}"
env >> {name}.env
echo "$( date ): {name} started" >> {name}.log
{pre}
{launch}
{post}
echo "$( date ): {name} finished" >> {name}.log
"""

del(os, sys, pwd, socket, np, find)

