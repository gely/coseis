! collective routines - serial version
module process
implicit none
integer :: file_null
contains

! initialize
subroutine init_process(master)
use fortran_io
logical, intent(out) :: master
file_null = fio_file_null
master = .true.
end subroutine

! finalize
subroutine finalize_process
end subroutine

! process rank
subroutine rank(ip, ip3, nproc3)
integer, intent(out) :: ip, ip3(3)
integer, intent(in) :: nproc3(3)
ip = 0
ip3 = nproc3
ip3 = 0
end subroutine

! barrier
subroutine barrier
end subroutine

! broadcast chacacter string
subroutine cbroadcast(str)
character(*), intent(inout) :: str
str(1:1) = str(1:1)
end subroutine

! broadcast integer
subroutine ibroadcast(i)
integer, intent(inout) :: i
i = i
end subroutine

! broadcast real 1d
subroutine rbroadcast1(f1, coords)
real, intent(inout) :: f1(:)
integer, intent(in) :: coords(3)
integer :: i
f1 = f1
i = coords(1)
end subroutine

! broadcast real 4d
subroutine rbroadcast4(f4, coords)
real, intent(inout) :: f4(:,:,:,:)
integer, intent(in) :: coords(3)
integer :: i
f4 = f4
i = coords(1)
end subroutine

! reduce real 1d
subroutine rreduce1(f1out, f1, op)
real, intent(out) :: f1out(:)
real, intent(in) :: f1(:)
character(*), intent(in) :: op
character :: a
a = op(1:1)
f1out = f1
end subroutine

! reduce real 2d
subroutine rreduce2(f2out, f2, op)
real, intent(out) :: f2out(:,:)
real, intent(in) :: f2(:,:)
character(*), intent(in) :: op
character :: a
a = op(1:1)
f2out = f2
end subroutine

! scalar swap halo
subroutine scalar_swap_halo(f3, n)
real, intent(inout) :: f3(:,:,:)
integer, intent(in) :: n(3)
return
f3(1,1,1) = f3(1,1,1) - n(1) + n(1)
end subroutine

! vector swap halo
subroutine vector_swap_halo(f4, n)
real, intent(inout) :: f4(:,:,:,:)
integer, intent(in) :: n(3)
return
f4(1,1,1,1) = f4(1,1,1,1) - n(1) + n(1)
end subroutine

! 2d real input/output
subroutine rio2(fh, f2, mode, filename, mm, nn, oo, mpio)
use fortran_io
integer, intent(inout) :: fh
real, intent(inout) :: f2(:,:)
character(1), intent(in) :: mode
character(*), intent(in) :: filename
integer, intent(in) :: mm(:), nn(:), oo(:), mpio
integer :: i
if (any(nn < 1)) return
i = size(oo)
call frio2(fh, f2, mode, filename, mm(i), oo(i))
i = mpio + nn(1)
end subroutine

! 2d integer input/output
subroutine iio2(fh, f2, mode, filename, mm, nn, oo, mpio)
use fortran_io
integer, intent(inout) :: fh
integer, intent(inout) :: f2(:,:)
character(1), intent(in) :: mode
character(*), intent(in) :: filename
integer, intent(in) :: mm(:), nn(:), oo(:), mpio
integer :: i
if (any(nn < 1)) return
i = size(oo)
call fiio2(fh, f2, mode, filename, mm(i), oo(i))
i = mpio + nn(1)
end subroutine

! 1d real input/output
subroutine rio1(fh, f1, mode, filename, m, o, mpio)
use fortran_io
integer, intent(inout) :: fh
real, intent(inout) :: f1(:)
character (1), intent(in) :: mode
character (*), intent(in) :: filename
integer, intent(in) :: m, o, mpio
real :: f2(1,size(f1))
integer :: i
if (mode == 'w') f2(1,:) = f1
call frio2(fh, f2, mode, filename, m, o)
if (mode == 'r') f1 = f2(1,:)
i = mpio
end subroutine

! 1d integer input/output
subroutine iio1(fh, f1, mode, filename, m, o, mpio)
use fortran_io
integer, intent(inout) :: fh
integer, intent(inout) :: f1(:)
character(1), intent(in) :: mode
character(*), intent(in) :: filename
integer, intent(in) :: m, o, mpio
integer :: f2(1,size(f1))
integer :: i
if (mode == 'w') f2(1,:) = f1
call fiio2(fh, f2, mode, filename, m, o)
if (mode == 'r') f1 = f2(1,:)
i = mpio
end subroutine

end module

