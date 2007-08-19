% TPV7
  np       = [    1   1  16 ];
  np       = [    1   1  32 ];
  nn       = [  351 201 128 ];
  n1expand = [    0   0   0 ];
  n2expand = [    0   0   0 ];
  bc1      = [   10   0  10 ];
  bc2      = [   10  10  10 ];
  ihypo    = [    0  76   0 ];
  fixhypo  =     -1;
  xhypo    = [  0. 7500. 0. ];
  affine   = [ 1. 0. 0.   0. 1. 0.   0. 0. 1. ];
  nt  = 1500;
  dx  = 100.;
  dt  = .008;

  rho = { 2670. 'zone' 1 1 1   -1 -1  0 };
  vp  = { 6000. 'zone' 1 1 1   -1 -1  0 };
  vs  = { 3464. 'zone' 1 1 1   -1 -1  0 };
  rho = { 2670. 'zone' 1 1 0   -1 -1 -1 };
  vp  = { 5000. 'zone' 1 1 0   -1 -1 -1 };
  vs  = { 2887. 'zone' 1 1 0   -1 -1 -1 };
  gam = .1;
  hourglass = [ 1. 2. ];

  faultnormal = 3;
  vrup = -1.;
  dc  = 0.4;
  mud = .525;
  mus = 10000.;
  mus = { .677   'cube' -15001.    -1. -1.  15001. 15001. 1. };
  tn  = -120e6;
  ts1 = 70e6;
  ts1 = { 81.6e6 'cube'  -1501.  5999. -1.   1501.  9001. 1. };

  out = { 'x'    1   1 1 76  0   -1 -1 76  0 };
  out = { 'trup' 1   1 1  0 -1   -1 -1  0 -1 };

  out = { 'u'  1    91 1 101 0    91 1 101 1500 };
  out = { 'v'  1    91 1 101 0    91 1 101 1500 };
  out = { 'ts' 1    91 1 101 0    91 1 101 1500 };
  out = { 'tn' 1    91 1 101 0    91 1 101 1500 };
  out = { 'u'  1     0 1 101 0     0 1 101 1500 };
  out = { 'v'  1     0 1 101 0     0 1 101 1500 };
  out = { 'ts' 1     0 1 101 0     0 1 101 1500 };
  out = { 'tn' 1     0 1 101 0     0 1 101 1500 };
  out = { 'u'  1   -91 1 101 0   -91 1 101 1500 };
  out = { 'v'  1   -91 1 101 0   -91 1 101 1500 };
  out = { 'ts' 1   -91 1 101 0   -91 1 101 1500 };
  out = { 'tn' 1   -91 1 101 0   -91 1 101 1500 };
  out = { 'u'  1    91 0 101 0    91 0 101 1500 };
  out = { 'v'  1    91 0 101 0    91 0 101 1500 };
  out = { 'ts' 1    91 0 101 0    91 0 101 1500 };
  out = { 'tn' 1    91 0 101 0    91 0 101 1500 };
  out = { 'u'  1   -91 0 101 0   -91 0 101 1500 };
  out = { 'v'  1   -91 0 101 0   -91 0 101 1500 };
  out = { 'ts' 1   -91 0 101 0   -91 0 101 1500 };
  out = { 'tn' 1   -91 0 101 0   -91 0 101 1500 };

  out = { 'u'  1    91 1 102 0    91 1 102 1500 };
  out = { 'v'  1    91 1 102 0    91 1 102 1500 };
  out = { 'ts' 1    91 1 102 0    91 1 102 1500 };
  out = { 'tn' 1    91 1 102 0    91 1 102 1500 };
  out = { 'u'  1     0 1 102 0     0 1 102 1500 };
  out = { 'v'  1     0 1 102 0     0 1 102 1500 };
  out = { 'ts' 1     0 1 102 0     0 1 102 1500 };
  out = { 'tn' 1     0 1 102 0     0 1 102 1500 };
  out = { 'u'  1   -91 1 102 0   -91 1 102 1500 };
  out = { 'v'  1   -91 1 102 0   -91 1 102 1500 };
  out = { 'ts' 1   -91 1 102 0   -91 1 102 1500 };
  out = { 'tn' 1   -91 1 102 0   -91 1 102 1500 };
  out = { 'u'  1    91 0 102 0    91 0 102 1500 };
  out = { 'v'  1    91 0 102 0    91 0 102 1500 };
  out = { 'ts' 1    91 0 102 0    91 0 102 1500 };
  out = { 'tn' 1    91 0 102 0    91 0 102 1500 };
  out = { 'u'  1   -91 0 102 0   -91 0 102 1500 };
  out = { 'v'  1   -91 0 102 0   -91 0 102 1500 };
  out = { 'ts' 1   -91 0 102 0   -91 0 102 1500 };
  out = { 'tn' 1   -91 0 102 0   -91 0 102 1500 };

