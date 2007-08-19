% TPV3
  np       = [    1   1  32 ];
  np       = [    1   1  64 ];
  nn       = [ 1201 400 128 ];
  n1expand = [   50   0   0 ];
  n2expand = [   50   0   0 ];
  bc1      = [    0  10  10 ];
  bc2      = [    0  10  -2 ];
  ihypo    = [  551 200  -2 ];
  fixhypo  =     -2;
  xhypo    = [  25.  0.  0. ];
  affine   = [ 1. 1. 1.   0. 1. 0.   0. 0. 1. ];
  nt  = 3000;
  dx  =  50.;
  dt  = .004;

  rho = 2670.;
  vp  = 6000.;
  vs  = 3464.;
  gam = .2;
  gam = { .02 'cube' -15001. -7501. -4000.   15001. 7501. 4000. };
  hourglass = [ 1. 2. ];

  faultnormal = 3;
  vrup = -1.;
  dc  = 0.4;
  mud = .525;
  mus = 10000.;
  mus = { .677   'cube' -15001. -7501. -1.  15001. 7501. 1. };
  tn  = -120e6;
  ts1 = 70e6;
  ts1 = { 81.6e6 'cube'  -1501. -1501. -1.   1501. 1501. 1. };

  out = { 'x'     1   1  1 -1  0   -1 -1 -1  0 };
  out = { 'svm' 100   1  1  0  0   -1 -1  0 -1 };
  out = { 'tsm'  -1   1  1  0  0   -1 -1  0 -1 };
  out = { 'tn'    1   1  1  0 -1   -1 -1  0 -1 };
  out = { 'su'    1   1  1  0 -1   -1 -1  0 -1 };
  out = { 'psv'   1   1  1  0 -1   -1 -1  0 -1 };
  out = { 'trup'  1   1  1  0 -1   -1 -1  0 -1 };

  out = { 'tn'    1   1  0  0  0   -1  0  0 -1 };
  out = { 'tsm'   1   1  0  0  0   -1  0  0 -1 };
  out = { 'sam'   1   1  0  0  0   -1  0  0 -1 };
  out = { 'svm'   1   1  0  0  0   -1  0  0 -1 };
  out = { 'sl'    1   1  0  0  0   -1  0  0 -1 };

  out = { 'x'     1   1  1 -1  0   -1 -1 -1  0 };
  out = { 'pv2'   1   1  1 -1 -1   -1 -1 -1 -1 };
  out = { 'vm2' 100   1  1 -1  0   -1 -1 -1 -1 };
  out = { 'vm2'   1   1  0 -1  0   -1  0 -1 -1 };
  out = { 'vm2'   1   0  1 -1  0    0 -1 -1 -1 };

  timeseries = { 'su' -7499.    -1. 0. };
  timeseries = { 'sv' -7499.    -1. 0. };
  timeseries = { 'ts' -7499.    -1. 0. };
  timeseries = { 'su'    -1. -5999. 0. };
  timeseries = { 'sv'    -1. -5999. 0. };
  timeseries = { 'ts'    -1. -5999. 0. };
  timeseries = { 'su'  7499.     1. 0. };
  timeseries = { 'sv'  7499.     1. 0. };
  timeseries = { 'ts'  7499.     1. 0. };
  timeseries = { 'su'     1.  5999. 0. };
  timeseries = { 'sv'     1.  5999. 0. };
  timeseries = { 'ts'     1.  5999. 0. };
