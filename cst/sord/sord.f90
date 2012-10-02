! SORD main program
program sord

! modules
use collective
use globals
use parameters
use setup
use arrays
use grid_generation
use field_io_mod
use material_model
use kinematic_source
use dynamic_rupture
use material_resample
use time_integration
use stress
use acceleration
use utilities
use statistics
implicit none
integer :: jp = 0, fh(9)
real :: prof0(14) = 0.0
real, allocatable :: prof(:,:)

! initialization
iotimer = 0.0
prof0(1) = timer(0)
call initialize(np0, ip);        master = ip == 0; prof0(1)  = timer(6)
call read_parameters;                              prof0(2)  = timer(6)
call setup_dimensions;     if (sync) call barrier; prof0(3)  = timer(6)
if (master) write (*, '(a)') 'SORD - Support Operator Rupture Dynamics'
call allocate_arrays;      if (sync) call barrier; prof0(4)  = timer(6)
call init_grid;            if (sync) call barrier; prof0(5)  = timer(6)
call init_material;        if (sync) call barrier; prof0(6)  = timer(6)
call init_pml;             if (sync) call barrier; prof0(7)  = timer(6)
call init_finite_source;   if (sync) call barrier; prof0(8)  = timer(6)
call init_rupture;         if (sync) call barrier; prof0(9)  = timer(6)
call resample_material;    if (sync) call barrier; prof0(10) = timer(6)
fh = -1
if (mpout /= 0) fh = file_null
allocate (prof(8,itio))
prof0(11) = iotimer
prof0(12) = timer(7)
if (master) call rio1(fh(9), prof0, 'w', 'prof-main.bin', 16, 0, mpout, verb)
prof0(12) = timer(7)

! main loop
if (master) write (*, '(a,i6,a)') 'Main loop:', nt, ' steps'
loop: do while (it < nt)
it = it + 1
jp = jp + 1
mptimer = 0.0
iotimer = 0.0
prof(1,jp) = timer(5)
call step_time;           if (sync) call barrier; prof(1,jp) = timer(5)
call step_stress;         if (sync) call barrier; prof(2,jp) = timer(5)
call step_accel;          if (sync) call barrier; prof(3,jp) = timer(5)
call stats;               if (sync) call barrier; prof(4,jp) = timer(5)
prof(6,jp) = mptimer
prof(7,jp) = iotimer
prof(8,jp) = timer(6)
if (it == nt .or. modulo(it, itio) == 0) then
    if (master) then
        call rio1(fh(1), prof(1,:jp), 'w', 'prof-1time.bin',   nt, it-jp, mpout, verb)
        call rio1(fh(2), prof(2,:jp), 'w', 'prof-2stress.bin', nt, it-jp, mpout, verb)
        call rio1(fh(3), prof(3,:jp), 'w', 'prof-3accel.bin',  nt, it-jp, mpout, verb)
        call rio1(fh(4), prof(4,:jp), 'w', 'prof-4stats.bin',  nt, it-jp, mpout, verb)
        call rio1(fh(6), prof(6,:jp), 'w', 'prof-6mp.bin',     nt, it-jp, mpout, verb)
        call rio1(fh(7), prof(7,:jp), 'w', 'prof-7io.bin',     nt, it-jp, mpout, verb)
        call rio1(fh(8), prof(8,:jp), 'w', 'prof-8step.bin',   nt, it-jp, mpout, verb)
        open (1, file='currentstep', status='replace')
        write (1, '(i6)') it
        close (1)
    end if
    jp = 0
end if
if (it == itstop) stop
end do loop

! finish up
if (sync) call barrier
prof0(1) = timer(7)
prof0(2) = timer(8)
if (master) then
    call rio1(fh(9), prof0(:2), 'w', 'prof-main.bin', 16, 14, mpout, verb)
    write (*, '(a)') 'Finished!'
end if
call finalize

end program
