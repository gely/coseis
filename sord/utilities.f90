! miscellaneous utilities
module utilities
implicit none
integer :: clockrate, clock0, timers(4)
contains

! clock timer
integer function clock()
call system_clock(clock)
clock = clock - clock0
end function

! array copy
subroutine rcopy(f, g, n)
real, intent(in) :: f(n)
real, intent(out) :: g(n)
integer, intent(in) :: n
integer :: i
!$omp parallel do schedule(static) private(i)
do i = 1, n
    g(i) = f(i)
end do
!$omp end parallel do
end subroutine

! array fill
subroutine rfill(f, r, n)
real, intent(inout) :: f(n)
real, intent(in) :: r
integer, intent(in) :: n
integer :: i
!$omp parallel do schedule(static) private(i)
do i = 1, n
    f(i) = r
end do
!$omp end parallel do
end subroutine

! array reciprocal
subroutine rinvert(f, n)
real, intent(inout) :: f(n)
integer, intent(in) :: n
integer :: i
!$omp parallel do schedule(static) private(i)
do i = 1, n
    if (f(i) /= 0.0) f(i) = 1.0 / f(i)
end do
!$omp end parallel do
end subroutine

! limit real array to min/max range
subroutine rlimits(f, fmin, fmax, n)
real, intent(inout) :: f(n)
real, intent(in) :: fmin, fmax
integer, intent(in) :: n
integer :: i
if (fmin > 0.0 .and. fmax > 0.0) then
    !$omp parallel do schedule(static) private(i)
    do i = 1, n
        f(i) = max(min(f(i), fmax), fmin)
    end do
    !$omp end parallel do
elseif (fmin > 0.0) then
    !$omp parallel do schedule(static) private(i)
    do i = 1, n
        f(i) = max(f(i), fmin)
    end do
    !$omp end parallel do
elseif (fmax > 0.0) then
    !$omp parallel do schedule(static) private(i)
    do i = 1, n
        f(i) = min(f(i), fmax)
    end do
    !$omp end parallel do
end if
end subroutine

! average of local eight values
subroutine average(f2, f1, i1, i2, d)
real, intent(out) :: f2(:,:,:)
real, intent(in) :: f1(:,:,:)
integer, intent(in) :: i1(3), i2(3), d
integer :: n(3), j, k, l
n = (/size(f1,1), size(f1,2), size(f1,3)/)
if (any(i1 < 1 .or. i2 > n)) stop 'error in average'
!$omp parallel do schedule(static) private(j, k, l)
do l = i1(3), i2(3)
do k = i1(2), i2(2)
do j = i1(1), i2(1)
    f2(j,k,l) = 0.125 * &
    ( f1(j,k,l) + f1(j+d,k+d,l+d) &
    + f1(j,k+d,l+d) + f1(j+d,k,l) &
    + f1(j+d,k,l+d) + f1(j,k+d,l) &
    + f1(j+d,k+d,l) + f1(j,k,l+d) )
end do
end do
end do
!$omp end parallel do
call set_halo(f2, 0.0, i1, i2)
end subroutine

! set array to real value outside specified region
subroutine set_halo(f, r, i1, i2)
real, intent(inout) :: f(:,:,:)
real, intent(in) :: r
integer, intent(in) :: i1(3), i2(3)
integer :: n(3), i3(3), i4(3)
n = (/size(f,1), size(f,2), size(f,3)/)
i3 = min(i1, n + 1)
i4 = max(i2, 0)
if (n(1) > 1) f(:i3(1)-1,:,:) = r
if (n(2) > 1) f(:,:i3(2)-1,:) = r
if (n(3) > 1) f(:,:,:i3(3)-1) = r
if (n(1) > 1) f(i4(1)+1:,:,:) = r
if (n(2) > 1) f(:,i4(2)+1:,:) = r
if (n(3) > 1) f(:,:,i4(3)+1:) = r
end subroutine

! L2 vector norm
subroutine vector_norm(f, w, i1, i2, di)
real, intent(out) :: f(:,:,:)
real, intent(in) :: w(:,:,:,:)
integer, intent(in) :: i1(3), i2(3), di(3)
integer :: n(3), j, k, l
n = (/size(f,1), size(f,2), size(f,3)/)
if (any(i1 < 1 .or. i2 > n)) stop 'error in vector_norm'
!$omp parallel do schedule(static) private(j, k, l)
do l = i1(3), i2(3), di(3)
do k = i1(2), i2(2), di(2)
do j = i1(1), i2(1), di(1)
    f(j,k,l) = &
    ( w(j,k,l,1) * w(j,k,l,1) &
    + w(j,k,l,2) * w(j,k,l,2) &
    + w(j,k,l,3) * w(j,k,l,3) )
end do
end do
end do
!$omp end parallel do
end subroutine

! Frobenius tensor norm - much faster than L2 norm for tensors
subroutine tensor_norm(f, w1, w2, i1, i2, di)
real, intent(out) :: f(:,:,:)
real, intent(in) :: w1(:,:,:,:), w2(:,:,:,:)
integer, intent(in) :: i1(3), i2(3), di(3)
integer :: n(3), j, k, l
n = (/size(f,1), size(f,2), size(f,3)/)
if (any(i1 < 1 .or. i2 > n)) stop 'error in tensor_norm'
!$omp parallel do schedule(static) private(j, k, l)
do l = i1(3), i2(3), di(3)
do k = i1(2), i2(2), di(2)
do j = i1(1), i2(1), di(1)
    f(j,k,l) = &
    ( w1(j,k,l,1) * w1(j,k,l,1) &
    + w1(j,k,l,2) * w1(j,k,l,2) &
    + w1(j,k,l,3) * w1(j,k,l,3) ) &
    + 2.0 * &
    ( w2(j,k,l,1) * w2(j,k,l,1) &
    + w2(j,k,l,2) * w2(j,k,l,2) &
    + w2(j,k,l,3) * w2(j,k,l,3) )
end do
end do
end do
!$omp end parallel do
end subroutine

! in-place linear interpolation
subroutine interpolate(f, i3, i4, di)
real, intent(inout) :: f(:,:,:)
integer, intent(in) :: i3(3), i4(3), di(3)
integer :: i1(3), i2(3), n(3), i, j, k, l, d
real :: h1, h2
n = (/size(f,1), size(f,2), size(f,3)/)
i1 = i3
i2 = i4
where (i1 < 1) i1 = i1 + (-i1 / di + 1) * di
where (i2 > n) i2 = i1 + (n - i1) / di * di
d = di(1)
do i = 1, d - 1
    h1 = 1.0 / d * i
    h2 = 1.0 / d * (d - i)
    !$omp parallel do schedule(static) private(j, k, l)
    do l = i1(3), i2(3), di(3)
    do k = i1(2), i2(2), di(2)
    do j = i1(1), i2(1) - d, d
        f(j+i,k,l) = h1 * f(j,k,l) + h2 * f(j+d,k,l)
    end do
    end do
    end do
    !$omp end parallel do
end do
d = di(2)
do i = 1, d - 1
    h1 = 1.0 / d * i
    h2 = 1.0 / d * (d - i)
    !$omp parallel do schedule(static) private(j, k, l)
    do l = i1(3), i2(3), di(1)
    do k = i1(2), i2(2) - d, d
    do j = i1(1), i2(1)
        f(j,k+i,l) = h1 * f(j,k,l) + h2 * f(j,k+d,l)
    end do
    end do
    end do
    !$omp end parallel do
end do
d = di(3)
do i = 1, d - 1
    h1 = 1.0 / d * i
    h2 = 1.0 / d * (d - i)
    !$omp parallel do schedule(static) private(j, k, l)
    do l = i1(3), i2(3) - d, d
    do k = i1(2), i2(2)
    do j = i1(1), i2(1)
        f(j,k,l+i) = h1 * f(j,k,l) + h2 * f(j,k,l+d)
    end do
    end do
    end do
    !$omp end parallel do
end do
end subroutine

! pulse time function
real function time_function(pulse, t, dt, tau)
character(*), intent(in) :: pulse
real, intent(in) :: t, dt, tau
real, parameter :: pi = 3.14159265
real :: f, a, b
f = 0.0
select case (pulse)
case ('const')
    f = 1.0
case ('delta')
    if (abs(t) < 0.25 * dt) f = 1.0 / dt
case ('step', 'integral_delta')
    if (abs(t) < 0.25 * dt) then
        f = 0.5
    elseif (t >= 0.25 * dt) then
        f = 1.0
    endif
case ('brune')
    if (0.0 < t) then
        a = 1.0 / tau
        f = exp(-a * t) * a * a * t
    endif
case ('integral_brune')
    if (0.0 < t) then
        a = 1.0 / tau
        f = 1.0 - exp(-a * t) * (a * t + 1.0)
    endif
case ('hann')
    b = pi * tau
    if (-b < t .and. t < b) then
        a = 1.0 / tau
        f = 0.5 / pi * a * (1.0 + cos(a * t))
    end if
case ('integral_hann')
    b = pi * tau
    if (-b < t .and. t < b) then
        a = 1.0 / tau
        f = 0.5 + 0.5 / pi * (a * t + sin(a * t))
    elseif (0.0 < t) then
        f = 1.0
    endif
case ('gaussian', 'integral_ricker1')
    a = 0.5 / (tau * tau)
    b = sqrt(a / pi)
    f = exp(-a * t * t) * b
case ('ricker1', 'integral_ricker2')
    a = 0.5 / (tau * tau)
    b = sqrt(a / pi) * 2.0 * a
    f = -exp(-a * t * t) * b * t
case ('ricker2')
    a = 0.5 / (tau * tau)
    b = sqrt(a / pi) * 4.0 * a
    f = exp(-a * t * t) * b * (a * t * t - 0.5)
case default
    write (0,*) 'invalid time func: ', trim(pulse)
    stop
end select
time_function = f
end function

end module

