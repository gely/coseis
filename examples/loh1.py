#!/usr/bin/env python
"""
PEER LOH.1 - Layer over a halfspace, buried double couple source
"""

import sord

np3 = 1, 16, 1			# number of processors in each dimension
nn = 261, 301, 161		# number of mesh nodes, nx ny nz
dx = 50., 50., 50.		# spatial step size
nt = 2251			# number of time steps
dt = 0.004			# time step size

# Material properties
hourglass = 1., 2.		# hourglass stiffness and viscosity
fieldio = [
    ( '=', 'rho', [], 2700. ),	# density
    ( '=', 'vp',  [], 6000. ),	# P-wave speed
    ( '=', 'vs',  [], 3464. ),	# S-wave speed
    ( '=', 'gam', [],    0. ),	# viscosity
]

# Material properties of the layer
fieldio += [
    ( '=', 'rho', [(),(),(1,21),()], 2600. ),
    ( '=', 'vp',  [(),(),(1,21),()], 4000. ),
    ( '=', 'vs',  [(),(),(1,21),()], 2000. ),
]

# Near side boundary conditions:
# Anti-mirror symmetry at the near x and y boundaries
# Free surface at the near z boundary
bc1 = -2, -2, 0	

# Far side boundary conditions:
# PML absorbing boundaries at x, y and z boundaries
bc2 = 10, 10, 10

# Source parameters
faultnormal = 0			# disable rupture dynamics
ihypo = 1, 1, 41		# hypocenter indices
xhypo = 0., 0., 2000.		# hypocenter coordinates
fixhypo = -2			# fix source at element center
rfunc = 'point'			# spatial function: point source
rsource = 0.5 * dx		# spatial function radius
tfunc = 'brune'			# time function: Brune pulse
tsource = 0.1			# time function dominant period
moment1 = 0., 0., 0.		# moment tensor M_xx, M_yy, M_zz
moment2 = 0., 0., 1e18		# moment tensor M_yz, M_zx, M_yz

# Velocity time series output for surface station
fieldio += [
    ( '=wx', 'v1', [], 'vx', (5999., 7999., -1.) ),
    ( '=wx', 'v2', [], 'vy', (5999., 7999., -1.) ),
    ( '=wx', 'v3', [], 'vz', (5999., 7999., -1.) ),
]

sord.run( locals() )

