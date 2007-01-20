% PEER UHS.1, UHS.2, LOH.1, 

  timeseries = { 'v'  600.  800. -2000. };
  timeseries = { 'v' 1200. 1600. -2000. };
  timeseries = { 'v' 1800. 2400. -2000. };
  timeseries = { 'v' 2400. 3200. -2000. };
  timeseries = { 'v' 3000. 4000. -2000. };
  timeseries = { 'v' 3600. 4800. -2000. };
  timeseries = { 'v' 4200. 5600. -2000. };
  timeseries = { 'v' 4800. 6400. -2000. };
  timeseries = { 'v' 5400. 7200. -2000. };
  timeseries = { 'v' 6000. 8000. -2000. };
% out = { 'x'  0   1 1 -1  0  -1 -1 -1  0 };
% out = { 'v' 10   1 1 -1 40  -1 -1 -1 -1 };
% out = { 'x'  0   1 1  0  0  -1 -1  0  0 };
% out = { 'v' 10   1 1  0 40  -1 -1  0 -1 };
% out = { 'x'  0   1 1  1  0  -1  1 -1  0 };
% out = { 'v' 10   1 1  1 40  -1  1 -1 -1 };
% out = { 'x'  0   1 1  1  0   1 -1 -1  0 };
% out = { 'v' 10   1 1  1 40   1 -1 -1 -1 };

  faultnormal = 0;
  moment1 = [ 0. 0. 0. ];
  moment2 = [ 0. 0. 1e18 ];
  tfunc = 'brune';
  rfunc = 'box';
  rfunc = 'tent';
  fixhypo = 2; rsource = 50.;
  fixhypo = 1; rsource = 100.;
  tsource = .1;

  dx  = 100;
  dt  = .008;
  upvector = [ 0 0 -1 ];
  origin = 0;
  gam = .0;
  hourglass = [ 1. 3. ];
  ihypo    = [   1   1  21 ];
  bc1      = [  -3  -3   0 ];
  n1expand = [   0   0   0 ];
  bc2      = [   0   0   0 ];
  n2expand = [  20  20  20 ];
  rexpand = 1.06;
  itcheck = 0;
  np  = [ 1 1 2 ];
  debug = 1;

  nt  = 1125;
  nt  = 625;
  nn  = [ 161 161 181 ];
  nn  = [ 111 111 81 ];

  vp  = 6000.;
  vs  = 3464.;
  rho = 2700.;
% vp  = { 4000. 'zone'   1 1 1   -1 -1 11 };
% vs  = { 2000. 'zone'   1 1 1   -1 -1 11 };
% rho = { 2600. 'zone'   1 1 1   -1 -1 11 };

