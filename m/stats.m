% Plot SORD statistics

function stats( varargin )
meta
runmeta
currentstep
tlim = [ 0 it*dt ];
cs = 'w0';
for i = 1:nargin
  arg = varargin{i};
  if ischar( arg )
    cs = arg;
  else
    tlim = arg;
  end
end
set( 0, 'ScreenPixelsPerInch', 150 )

f = readf32( 'prof/comp' );
if ~isempty( f )
  g = -f + readf32( 'prof/step' );
  figure(1); clf
  colorscheme( cs )
  pos = get( gcf, 'Pos' );
  set( gcf, 'PaperPositionMode', 'auto', 'Pos', [ pos(1:2) 640 640 ] )
  axes( 'Pos', [ .13 .57 .84 .4 ] )
  %plot( sqrt( f ), '.', 'MarkerE', [ 0 0 .5 ] ), hold on
  %plot( sqrt( g ), '.', 'MarkerE', [ .5 0 0 ] )
  plot( f, '.', 'MarkerE', [ 0 0 .5 ] ), hold on
  plot( g, '.', 'MarkerE', [ .5 0 0 ] )
  xlim( tlim ./ dt )
  ptitle( [ 'NP=' num2str( prod( np ) ) ] )
  ylabel( 'Step Time (s)' )
  set( gca, 'XTickLabel', [] )
  legend( { 'Computation' 'Overhead' }, 'Location', 'North' )
  legend boxoff
  f = cumsum( f ) / 3600;
  g = cumsum( g ) / 3600;
  axes( 'Pos', [ .13 .13 .84 .4 ] )
  area( [ f g ] )
  xlim( tlim ./ dt )
  ptitle( [ 'NP=' num2str( prod( np ) ) ] )
  xlabel( 'Step' )
  ylabel( 'Cumulative Run Time (hr)' )
  legend( { 'Computation' 'Overhead' }, 'Location', 'North' )
  legend boxoff
  colormap jet
  printpdf( 'prof' )
end

figure(2); clf
colorscheme( cs )
pos = get( gcf, 'Pos' );
set( gcf, 'PaperPositionMode', 'auto', 'Pos', [ pos(1:2) 640 640 ] )
set( gcf, 'DefaultLineLinewidth', 1 )
axes( 'Pos', [ .13 .71 .84 .26 ] )
f = readf32( 'stats/umax' );
t = ( 1:length(f) ) * dt * itstats;
plot( t, f )
xlim( tlim )
ptitle( 'Max Displacement' )
ylabel( 'u (m)' )
set( gca, 'XTickLabel', [] )
axes( 'Pos', [ .13 .42 .84 .26 ] )
f = readf32( 'stats/vmax' );
plot( t, f )
xlim( tlim )
ptitle( 'Max Velocity', 'r' )
ylabel( 'u'' (m/s)' )
set( gca, 'XTickLabel', [] )
axes( 'Pos', [ .13 .13 .84 .26 ] )
f = readf32( 'stats/amax' );
plot( t, f )
xlim( tlim )
ptitle( 'Max Acceleration', 'r' )
xlabel( 'Time (s)' )
ylabel( 'u'''' (m/s^2)' )
printpdf( 'disp' )

if faultnormal

figure(3); clf
colorscheme( cs )
pos = get( gcf, 'Pos' );
set( gcf, 'PaperPositionMode', 'auto', 'Pos', [ pos(1:2) 640 640 ] )
set( gcf, 'DefaultLineLinewidth', 1 )
axes( 'Pos', [ .13 .71 .84 .26 ] )
f = readf32( 'stats/sumax' );
t = ( 1:length(f) ) * dt * itstats;
plot( t, f )
xlim( tlim )
ptitle( 'Max Slip' )
ylabel( 's (m)' )
set( gca, 'XTickLabel', [] )
axes( 'Pos', [ .13 .42 .84 .26 ] )
f = readf32( 'stats/svmax' );
plot( t, f )
xlim( tlim )
ptitle( 'Max Slip Rate', 'r' )
ylabel( 's'' (m/s)' )
set( gca, 'XTickLabel', [] )
axes( 'Pos', [ .13 .13 .84 .26 ] )
f = readf32( 'stats/samax' );
plot( t, f )
xlim( tlim )
ptitle( 'Max Slip Acceleration', 'r' )
xlabel( 'Time (s)' )
ylabel( 's'''' (m/s^2)' )
printpdf( 'slip' )

figure(4); clf
colorscheme( cs )
pos = get( gcf, 'Pos' );
set( gcf, 'PaperPositionMode', 'auto', 'Pos', [ pos(1:2) 640 640 ] )
set( gcf, 'DefaultLineLinewidth', 1 )
axes( 'Pos', [ .13 .13 .84 .84 ] )
plot( tlim, [ 0 0 ], '--', 'HandleVisibility', 'off' ), hold on
f = readf32( 'stats/tsmax' ); plot( t, 1e-6 * f )
f = readf32( 'stats/tnmax' ); plot( t, 1e-6 * f, 'r' )
f = readf32( 'stats/tnmin' ); plot( t, 1e-6 * f, 'b' )
xlim( tlim )
xlabel( 'Time (s)' )
ylabel( 'Stress (MPa)' )
legend( { 'Max |\tau_s|' 'Max \sigma_n' 'Min \sigma_n' }, 'Location', 'NorthWest' )
legend boxoff
printpdf( 'stress' )

figure(5); clf
colorscheme( cs )
pos = get( gcf, 'Pos' );
set( gcf, 'PaperPositionMode', 'auto', 'Pos', [ pos(1:2) 640 640 ] )
set( gcf, 'DefaultLineLinewidth', 1 )
axes( 'Pos', [ .13 .57 .84 .4 ] )
f = diff( readf32( 'stats/moment' ) ) / dt;
t = ( 1:length(f) ) * dt * itstats;
plot( t, 1e-18 * f )
xlim( tlim )
y = ylim; ylim( [ 0 y(2) ] )
ptitle( 'Moment Rate', 'r' )
ylabel( 'EN-m/s' )
set( gca, 'XTickLabel', [] )
axes( 'Pos', [ .13 .13 .84 .4 ] )
f = diff( readf32( 'stats/efric' ) ) / dt;
plot( t, 1e-15 * f )
xlim( tlim )
y = ylim; ylim( [ 0 y(2) ] )
ptitle( 'Dissipated Power', 'r' )
xlabel( 'Time (s)' )
ylabel( 'Power (PW)' )
printpdf( 'energy' )

end

