#!/usr/bin/env python
"""
Kostrov constant rupture velocity test
"""

import sys
sys.path.insert( 0, '../..' )
import sord

np = 1, 1, 1
nt = 400
_j, _k, _l = 61, 61, 21
ihypo = _j, _k, _l
nn = 2*_j, 2*_k, 2*_l
bc1 = 10, 10, 10
bc2 = 10, 10, 10
faultnormal = 3
vrup = 3117.6914
rcrit = 1e9
trelax = 0.

fieldio = [
    ( '=',  'mus', [],    1e9 ),
    ( '=',  'mud', [],    0.  ),
    ( '=',  'dc',  [],    1e9 ),
    ( '=',  'co',  [],    0.  ),
    ( '=',  'tn',  [], -100e6 ),
    ( '=',  'ts',  [],  -90e6 ),
    ( '=w', 'sl',  [ 0, 0, 0, -1 ],         'sl'  ),
    ( '=w', 'svm', [ 0, 0, 0, -1 ],         'svm' ),
    ( '=w', 'x1',  [ 0, 0, _l ,0 ],         'x1'  ),
    ( '=w', 'x2',  [ 0, 0, _l ,0 ],         'x2'  ),
    ( '=w', 'x3',  [ 0, 0, _l ,0 ],         'x3'  ),
    ( '=w', 'v1',  [ 0, 0, _l, (1,-1,20) ], 'v1'  ),
    ( '=w', 'v2',  [ 0, 0, _l, (1,-1,20) ], 'v2'  ),
    ( '=w', 'v3',  [ 0, 0, _l, (1,-1,20) ], 'v3'  ),
]

sord.run( locals() )
