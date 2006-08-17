! Lock nodes by setting acceleration to zero
module m_locknodes
implicit none
contains

subroutine locknodes
use m_globals
use m_zone
integer :: i1(3), i2(3), i, j1, k1, l1, j2, k2, l2, iz
logical, save :: init = .true.

if ( init ) then
  if ( nlock > nz ) then
    write( 0, * ) 'too many lock zones, make nz bigger ', nlock, nz
    stop 
  end if
  do iz = 1, nlock
    i1 = i1lock(iz,:)
    i2 = i2lock(iz,:)
    call zone( i1, i2, nn, nnoff, ihypo, faultnormal )
    i1lock(iz,:) = max( i1, i2node )
    i2lock(iz,:) = min( i2, i2node )
  end do
end if

do iz = 1, nlock
  i1 = i1lock(iz,:)
  i2 = i2lock(iz,:)
  j1 = i1(1); j2 = i2(1)
  k1 = i1(2); k2 = i2(2)
  l1 = i1(3); l2 = i2(3)
  do i = 1, 3
    if ( ilock(iz,i) == 1 ) w1(j1:j2,k1:k2,l1:l2,i) = 0.
  end do
end do

end subroutine

end module

