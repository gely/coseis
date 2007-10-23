% TPV3
  np       = [    1   1  16 ];
  np       = [    1   1  32 ];
  nn       = [  351 201 128 ];
  n1expand = [    0   0   0 ];
  n2expand = [    0   0   0 ];
  bc1      = [   10  10  10 ];
  bc2      = [   -1   1  -2 ];
  ihypo    = [   -1  -1  -2 ];
  fixhypo  =     -1;
  xhypo    = [   0.  0.  0. ];
  affine   = [ 1. 0. 0.   0. 1. 0.   0. 0. 1. ];
  nt  = 3000;
  dx  = 50.;
  dt  = 0.004;

  rho = 2670.;
  vp  = 6000.;
  vs  = 3464.;
  gam = 0.2;
  gam = { 0.02 'cube' -15001. -7501. -4000.   15001. 7501. 4000. };
  hourglass = [ 1. 2. ];

  faultnormal = 3;
  vrup = -1.;
  dc  = 0.4;
  mud = 0.525;
  mus = 10000.;
  mus = { 0.677  'cube' -15001. -7501. -1.  15001. 7501. 1. };
  tn  = -120e6;
  ts1 = 70e6;
  ts1 = { 72.9e6 'cube'  -1501. -1501. -1.   1501. 1501. 1. };
  ts1 = { 75.8e6 'cube'  -1501. -1499. -1.   1501. 1499. 1. };
  ts1 = { 75.8e6 'cube'  -1499. -1501. -1.   1499. 1501. 1. };
  ts1 = { 81.6e6 'cube'  -1499. -1499. -1.   1499. 1499. 1. };

  out = { 'x'     1   51 51  -2  0    -1 -1  -2  0 };
  out = { 'svm' 100   51 51   0 -1    -1 -1   0 -1 };
  out = { 'tsm'  -1   51 51   0  0    -1 -1   0 -1 };
  out = { 'tn'    1   51 51   0 -1    -1 -1   0 -1 };
  out = { 'su'    1   51 51   0 -1    -1 -1   0 -1 };
  out = { 'psv'   1   51 51   0 -1    -1 -1   0 -1 };
  out = { 'trup'  1   51 51   0 -1    -1 -1   0 -1 };

  out = { 'tn'    1   51  0   0  0    -1  0   0 -1 };
  out = { 'tsm'   1   51  0   0  0    -1  0   0 -1 };
  out = { 'sam'   1   51  0   0  0    -1  0   0 -1 };
  out = { 'svm'   1   51  0   0  0    -1  0   0 -1 };
  out = { 'sl'    1   51  0   0  0    -1  0   0 -1 };

  out = { 'x'     1    1  1  -2  0    -1 -1  -2  0 };
  out = { 'pv2'   1    1  1  -2 -1    -1 -1  -2 -1 };
  out = { 'vm2' 100    1  1  -2  0    -1 -1  -2 -1 };
  out = { 'vm2'   1    1  0  -2  0    -1  0  -2 -1 };
  out = { 'vm2'   1    0  1  -2  0     0 -1  -2 -1 };

  timeseries = { 'su' -7500.     0. 0. };
  timeseries = { 'sv' -7500.     0. 0. };
  timeseries = { 'ts' -7500.     0. 0. };
  timeseries = { 'su'     0. -6000. 0. };
  timeseries = { 'sv'     0. -6000. 0. };
  timeseries = { 'ts'     0. -6000. 0. };
  timeseries = { 'su' -7450.   -50. 0. };
  timeseries = { 'sv' -7450.   -50. 0. };
  timeseries = { 'ts' -7450.   -50. 0. };
  timeseries = { 'su'   -50. -5950. 0. };
  timeseries = { 'sv'   -50. -5950. 0. };
  timeseries = { 'ts'   -50. -5950. 0. };

