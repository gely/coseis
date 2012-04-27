"""
USC HPC - http://www.usc.edu/hpcc/

.login
source /usr/usc/globus/default/setup.csh
#source /usr/usc/mpich/default/setup.csh
source /usr/usc/mpich2/1.3.1..10/setup.csh
setenv F77 gfortran
setenv F90 gfortran

Do not add to the front of your path.

alias qme='qstat -u $USER"'
alias qdev='qsub -I -l nodes=1,walltime=1:00:00'
pbsnodes -a | grep main | sort | uniq -c

Use /home instead of /auto
I/O to temporary space: /scratch
Use autogenerated sync.sh to check job during run.
mpiexec does not seem to work on interactive node, so using mpirun.
"""
login = 'hpc-login2.usc.edu'
hostname = 'hpc.*'
rate = 1.1e6
queue = 'default'
queue_opts = [
  ('default',  {'maxnodes': 256, 'maxcores': 8, 'maxram': 11000, 'maxtime':  (24, 00)}),
  ('default',  {'maxnodes': 256, 'maxcores': 4, 'maxram':  3500, 'maxtime':  (24, 00)}),
  ('largemem', {'maxnodes':   1, 'maxcores': 8, 'maxram': 63000, 'maxtime': (336, 00)}),
  ('nbns',     {'maxnodes':  48, 'maxcores': 8, 'maxram': 11000, 'maxtime': (336, 00)}),
]
launch = {
    's_exec':  '{command}',
    's_debug': 'gdb {command}',
    #'m_exec':  'mpirun -n {nproc} {command}',
    'm_exec':  'mpiexec -n {nproc} {command}',
    'submit':  'qsub "{name}.sh"',
    'submit2': 'qsub -W depend="afterok:{depend}" "{name}.sh"',
}

