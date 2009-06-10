#!/usr/bin/env python
"""
Elsinore simulation
"""
import sys, sord

projection = sord.coord.ll2xy
srf_ = 'data/cybershake/010-003-001-000'
vm_ = '1d'
vm_ = 'cvm'; topo_ = True
vm_ = 'uhs'; topo_ = False
T = 240.
L = 600000.0, 300000.0, -80000.0
dx =  200.0,  200.0,  -200.0 ; npml = 10 ; d = 2 ; np3 = 1, 40, 101 ; queue = None
dx =  500.0,  500.0,  -500.0 ; npml = 10 ; d = 1 ; np3 = 1, 1, 81   ; queue = None
dx = 2000.0, 2000.0, -2000.0 ; npml = 5  ; d = 1 ; np3 = 1, 1, 2    ; queue = None

if 0:
    bc1 = 10, 10, 0
    bc2 = 10, 10, 10
else:
    bc1 = 0, 0, 0
    bc2 = 0, 0, 0
    n1expand = 50, 50, 0
    n2expand = 50, 50, 50

dt = dx[0] / 12500.0
nt = int( T / dt + 1.00001 )
nn = [
    int( L[0] / dx[0] + 1.00001 ),
    int( L[1] / dx[1] + 1.00001 ),
    int( L[2] / dx[2] + 1.00001 ),
]
source = 'potency'
infiles = '~/run/tmp/src_*',
rundir  = '~/run/elsinore-' + vm_

# output
for f in 'x1', 'x2', 'x3', 'v1', 'v2', 'v3':
    fieldio += [ ( '=w', f, [(1, -1, d), (1, -1, d), 1, ()], f ) ]

# topography mesh
if topo_:
    fieldio += [ ( '=r', 'x3',  [], '~/run/tmp/zz' ) ]

# velocity model
hourglass = 1.0, 1.0
vp1 = 1500.0
vs1 = 500.0
vdamp = 400.0
gam2 = 0.8 
if vm_ == 'uhs':
    fieldio += [
        ( '=',  'rho', [], 2500.0 ),
        ( '=',  'vp',  [], 6000.0 ),
        ( '=',  'vs',  [], 3500.0 ),
    ]
elif vm_ == 'cvm':
    fieldio += [
        ( '=r', 'rho', [], '~/run/cvm4/rho' ),
        ( '=r', 'vp',  [], '~/run/cvm4/vp'  ),
        ( '=r', 'vs',  [], '~/run/cvm4/vs'  ),
    ]
elif vm_ == '1d':
    layers_ = [
        (  0.0, 5.5, 3.18, 2.4  ),
        (  5.5, 6.3, 3.64, 2.67 ),
        (  8.4, 6.3, 3.64, 2.67 ),
        ( 16.0, 6.7, 3.87, 2.8  ),
        ( 35.0, 7.8, 4.5,  3.0  ),
    ]
    for dep_, vp_, vs_, rho_ in layers_:
        i = int( -dep_ / dx[2] + 1.5 )
        fieldio += [
            ( '=', 'rho', [(), (), (i, -1), ()], 1000.0 * rho_ ),
            ( '=', 'vp',  [(), (), (i, -1), ()], 1000.0 * vp_  ),
            ( '=', 'vs',  [(), (), (i, -1), ()], 1000.0 * vs_  ),
        ]
else:
    sys.exit( 'bad vm' )

# run SORD job
if __name__ == '__main__':
    data = sord.source.srfb_read( srf_ )[1]
    nsource = sord.source.srf2potency( data, projection, (dx[0], dx[1], -dx[2]), '~/run/tmp' )
    sord.run( locals() )
