% Test

% affine = [ 1 0 0   1 1 0   0 0 1   1 ];

  debug = 1;
  itswap = 1;
  np = [ 1 5 1 ];
  nn = [ 8 4 8 ];

  nt = 10;
  dx = 100;
  dt = .0075;
  bc1 = [ 0 0 0 ];
  bc2 = [ 0 0 0 ];

  faultnormal = 0;
  moment1 = [ 1e16 1e16 1e16 ];
  moment2 = [ 0. 0. 0. ];
  ihypo = [ 3 3 3 ];
  fixhypo = 2;
  rsource = 50.;


