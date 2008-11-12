#!/usr/bin/env python
"""
Miniature point source problem
"""

import sys
sys.path.insert( 0, '../..' )
import sord

debug = 1
np = 2, 1, 1
nn = 2, 2, 2

hourglass = 0., 0.

nt = 10
dx = 100
dt = 0.0075
bc1 = 0, 0, 0
bc2 = 0, 0, 0

faultnormal = 0
moment1 = 1e16, 1e16, 1e16
moment2 = 0., 0., 0.
ihypo = 1, 1, 1
fixhypo = 2
affine = (1.,0.,0.), (1.,1.,0.), (0.,0.,1.)
rsource = 50.

fieldio = []
for _f in sord.fieldnames.volume:
    fieldio += [ ( '=w', _f, [], _f ) ]

sord.run( locals() )
