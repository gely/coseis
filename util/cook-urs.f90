! Cook URS ShakeOut data

program main
implicit none
real, parameter :: t0 = -2.0, dt0 = 0.2, dt = 0.2
!integer, parameter :: nn = 417*834, nt = 1200
integer, parameter :: nn = 250*500, nt = 1200
integer :: io, it0, it1, it = 1
real :: vx(nn), vy(nn), vz(nn), ux(nn), uy(nn), uz(nn), v(nn), pv(nn), pvh(nn), t

pv = 0.
pvh = 0.
inquire( iolength=io ) vx
open( 1, file='v1', recl=io, form='unformatted', access='direct', status='old' )
open( 2, file='v2', recl=io, form='unformatted', access='direct', status='old' )
open( 3, file='v3', recl=io, form='unformatted', access='direct', status='old' )
open( 4, file='vh', recl=io, form='unformatted', access='direct', status='replace' )
do it0 = 1, nt-1
  read( 1, rec=it0 ) vx
  read( 2, rec=it0 ) vy
  read( 3, rec=it0 ) vz
  ux = ux + dt * vx
  uy = uy + dt * vy
  uz = uz + dt * vz
  v = sqrt( vx * vx + vy * vy + vz * vz )
  pv = max( v, pv )
  v = sqrt( vx * vx + vy * vy )
  pvh = max( v, pvh )
  t = dt * ( it - 1 )
  it1 = nint( ( t - t0 ) / dt0 ) + 1
  it1 = max( it1, 1 )
  if ( it0 == it1 ) then
    print *, it, it0
    write( 4, rec=it ) v
    it = it + 1
  end if
end do
close( 1 )
close( 2 )
close( 3 )
close( 4 )

open( 1, file='u1',  recl=io, form='unformatted', access='direct', status='replace' )
open( 2, file='u2',  recl=io, form='unformatted', access='direct', status='replace' )
open( 3, file='u3',  recl=io, form='unformatted', access='direct', status='replace' )
write( 1, rec=1 ) ux
write( 2, rec=1 ) uy
write( 3, rec=1 ) uz
close( 1 )
close( 2 )
close( 3 )

open( 1, file='um',  recl=io, form='unformatted', access='direct', status='replace' )
open( 2, file='uh',  recl=io, form='unformatted', access='direct', status='replace' )
open( 3, file='pv',  recl=io, form='unformatted', access='direct', status='replace' )
open( 4, file='pvh', recl=io, form='unformatted', access='direct', status='replace' )
v = sqrt( ux * ux + uy * uy + uz * uz )
write( 1, rec=1 ) v
v = sqrt( ux * ux + uy * uy )
write( 2, rec=1 ) v
write( 3, rec=1 ) pv
write( 4, rec=1 ) pvh
close( 1 )
close( 2 )
close( 3 )
close( 4 )

end program
