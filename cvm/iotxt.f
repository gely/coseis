! ASCII I/O for SCEC CVM

      subroutine readpts( kerr )
      implicit none
      include 'newin.h'
      integer :: kerr, i
      character(160) :: str
      write( 0, '(a)' ) 'SCEC Community Velocity Model'
      call get_command_argument( 1, str )
      open( 1, file=str, status='old' )
      read( 1, * ) nn
      if ( nn > ibig ) then
         print *, 'Error: nn greater than ibig', nn , ibig
         stop
      end if
      do i = 1, nn
        read( 1, * ) rlat(i), rlon(i), rdep(i)
        if( rdep(i) .lt. 0 ) write( 0, * )
     $    'Error: degative depth', i, rlon(i), rlat(i), rdep(i)
        if(rlon(i)/=rlon(i).or.rlat(i)/=rlat(i).or.rdep(i)/=rdep(i))
     $    write( 0, * ) 'Error: NaN', i, rlon(i), rlat(i), rdep(i)
        rdep(i) = rdep(i) * 3.2808399
        if( rdep(i) .lt. rdepmin ) rdep(i) = rdepmin
      end do
      close( 1 )
      kerr = 0
      end

      subroutine writepts( kerr )
      implicit none
      include 'newin.h'
      integer :: kerr, i
      character(160) :: str
      call get_command_argument( 2, str )
      open( 1, file=str, status='replace' )
      do i = 1, nn
        rdep(i) = rdep(i) / 3.2808399
        write( 1, '(f8.5,1x,f10.5,1x,f9.2,1x,f8.1,1x,f8.1,1x,f8.1)' ) 
      end do
      close( 1 )
      kerr = 0
      end
