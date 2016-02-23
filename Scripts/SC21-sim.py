#!/usr/bin/env python3
"""
PEER Lifelines program task 1A02, Problem SC2.1
SCEC Community Velocity Model, version 2.2 with double-couple point source.
"""
import os
import json
import cst.sord

prm = {}

# parameters
dx = 2000.0; prm['nproc3'] = [1, 1, 1]
dx = 200.0;  prm['nproc3'] = [1, 2, 30]
dx = 100.0;  prm['nproc3'] = [1, 4, 60]
dx = 500.0;  prm['nproc3'] = [1, 1, 2]

# mesh metadata
mesh = cst.sord.repo + ('SC21-Mesh-%.0f' % dx) + os.sep
meta = json.load(open(mesh + 'meta.json'))
dx, dy, dz = meta['delta']
nx, ny, nz = meta['shape']

# dimensions
dt = dx / 16000.0
dt = dx / 20000.0
nt = int(50.0 / dt + 1.00001)
prm['delta'] = [dx, dy, dz, dt]
prm['shape'] = [nx, ny, nz, nt]

# boundary conditions
prm['bc1'] = ['pml', 'pml', 'free']
prm['bc2'] = ['pml', 'pml', 'pml']

# material
prm['rho'] = [([], '=<', 'mesh-rho.bin')]
prm['vp'] = [([], '=<', 'mesh-vp.bin')]
prm['vs'] = [([], '=<', 'mesh-vs.bin')]
prm['gam'] = [0.0]
prm['vp1'] = [600.0]
prm['vs1'] = [200.0]
prm['hourglass'] = [1.0, 1.0]

# source
j = int(56000.0 / dx + 0.5)
k = int(40000.0 / dx + 0.5)
l = int(14000.0 / dx + 0.5)
prm['mxy'] = ([j, k, l, []], '+', 1e18, 'brune', 0.2)

# receivers
for i in range(8):
    j = int((74000.0 - 6000.0 * i) / dx)
    k = int((16000.0 + 8000.0 * i) / dy)
    for f in 'vx', 'vy', 'vz':
        if f not in prm:
            prm[f] = []
        prm[f] += [
            ([j, k, 0, []], '=>', 'p%s-%s.bin' % (i, f)),
        ]

# run job
d = cst.sord.repo + 'PEER-SC2.1-%.0f' % dx
os.mkdir(d)
os.chdir(d)
for v in 'rho', 'vp', 'vs':
    os.link(mesh + 'mesh-' + v + '.bin', '.')
cst.sord.run(prm)
