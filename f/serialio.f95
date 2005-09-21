!------------------------------------------------------------------------------!
! SERIAL

module parallelio_m
contains

! Write scalar field
subroutine pwrite3( filename, s1, i1, i2, n, noff )
implicit none
character*(*), intent(in) :: filename
real, intent(in) :: s1(:,:,:)
integer, intent(in) :: i1(3), i2(3), n(3), noff(3)
integer :: j1, k1, l1, j2, k2, l2, reclen
j1 = i1(1); j2 = i2(1)
k1 = i1(2); k2 = i2(2)
l1 = i1(3); l2 = i2(3)
inquire( iolength=reclen ) s1(j1:j2,k1:k2,l1:l2)
if ( reclen == 0 ) return
open( 9, &
  file=filename, &
  recl=reclen, &
  form='unformatted', &
  access='direct', &
  status='replace' )
write( 9, rec=1 ) s1(j1:j2,k1:k2,l1:l2)
close( 9 )
end subroutine

! Write vector component
subroutine pwrite4( filename, w1, i1, i2, i, n, noff )
implicit none
character*(*), intent(in) :: filename
real, intent(in) :: w1(:,:,:,:)
integer, intent(in) :: i1(3), i2(3), i, n(3), noff(3)
integer :: j1, k1, l1, j2, k2, l2, reclen
j1 = i1(1); j2 = i2(1)
k1 = i1(2); k2 = i2(2)
l1 = i1(3); l2 = i2(3)
inquire( iolength=reclen ) w1(j1:j2,k1:k2,l1:l2,i)
if ( reclen == 0 ) return
open( 9, &
  file=filename, &
  recl=reclen, &
  form='unformatted', &
  access='direct', &
  status='replace' )
write( 9, rec=1 ) w1(j1:j2,k1:k2,l1:l2,i)
close( 9 )
end subroutine

! Read scalar field
subroutine pread3( filename, s1, i1, i2, n, noff )
implicit none
character*(*), intent(in) :: filename
real, intent(out) :: s1(:,:,:)
integer, intent(in) :: i1(3), i2(3), n(3), noff(3)
integer :: j1, k1, l1, j2, k2, l2, reclen
j1 = i1(1); j2 = i2(1)
k1 = i1(2); k2 = i2(2)
l1 = i1(3); l2 = i2(3)
inquire( iolength=reclen ) s1(j1:j2,k1:k2,l1:l2)
if ( reclen == 0 ) return
open( 9, &
  file=filename, &
  recl=reclen, &
  form='unformatted', &
  access='direct', &
  status='old' )
read( 9, rec=1 ) s1(j1:j2,k1:k2,l1:l2)
close( 9 )
end subroutine

! Read vector component
subroutine pread4( filename, w1, i1, i2, i, n, noff )
implicit none
character*(*), intent(in) :: filename
real, intent(out) :: w1(:,:,:,:)
integer, intent(in) :: i1(3), i2(3), i, n(3), noff(3)
integer :: j1, k1, l1, j2, k2, l2, reclen
j1 = i1(1); j2 = i2(1)
k1 = i1(2); k2 = i2(2)
l1 = i1(3); l2 = i2(3)
inquire( iolength=reclen ) w1(j1:j2,k1:k2,l1:l2,i)
if ( reclen == 0 ) return
open( 9, &
  file=filename, &
  recl=reclen, &
  form='unformatted', &
  access='direct', &
  status='old' )
read( 9, rec=1 ) w1(j1:j2,k1:k2,l1:l2,i)
close( 9 )
end subroutine

end module

