#!/usr/bin/env python
"""
SCEC Community Velocity Model (CVM-H) extraction tool
"""
import os, sys, urllib, pyproj
import numpy as np
import coord, gocad

# projection
proj = pyproj.Proj( proj='utm', zone=11, datum='NAD27', ellps='clrk66' )
extent = (131000.0, 828000.0), (3431000.0, 4058000.0), (-200000.0, 4900.0)

# lookup tables
property2d = {'topo': '1', 'base': '2', 'moho': '3'}
property3d = {'rho': '1', 'vp': '1', 'vs': '3', 'tag': '2'}
voxet3d = {'mantle': 'CVM_CM', 'crust': 'CVM_LR', 'lab': 'CVM_HR'}

def read_voxet( property=None, voxet=None ):
    """
    Download and read SCEC CVM-H voxet.

    Parameters
    ----------
        2d property: 'topo', 'base', or 'moho'
        3d property: 'rho', 'vp', 'vs', or 'tag'
        3d voxet: 'mantle', 'crust', 'lab'

    Returns
    -------
        extent: (x0, x1), (y0, y1), (z0, z1)
        delta: dx, dy, dz
        data: property voxet array
    """

    # download if not found
    repo = os.path.expanduser( '~/mapdata' )
    url = 'http://structure.harvard.edu/cvm-h/download/vx62.tar.bz2'
    version = os.path.basename( url ).split( '.' )[0]
    path = os.path.join( repo, version, 'bin' )
    if not os.path.exists( path ):
        if not os.path.exists( repo ):
            os.makedirs( repo )
        f = os.path.join( repo, os.path.basename( url ) )
        if not os.path.exists( f ):
            print( 'Downloading %s' % url )
            urllib.urlretrieve( url, f )
        if os.system( 'tar jxv -C %r -f %r' % (repo, f) ):
            sys.exit( 'Error extraction tar file' )

    # lookup property and voxet
    if property in property2d:
        property = property2d[property]
        voxet = 'interfaces'
    if property in property3d:
        property = property3d[property]
    if voxet in voxet3d:
        voxet = voxet3d[voxet]

    # load voxet
    f = os.path.join( path, voxet + '.vo' )
    voxet = gocad.voxet( f, property )['1']

    # extent
    x, y, z = voxet['AXIS']['O']
    u, v, w = voxet['AXIS']['U'][0], voxet['AXIS']['V'][1], voxet['AXIS']['W'][2]
    extent = (x, x + u), (y, y + v), (z, z + w)

    # data
    if property == None:
        return voxet, extent
    else:
        data = voxet['PROP'][property]['DATA']
        if property == 'rho':
            data *= 0.001
            data = 1000.0 * (data * (1.6612 + data * (-0.4721 + data * (0.0671 +
                f * (-0.0043 + data * 0.000106)))))
            data = np.maximum( data, 1000.0 )
        return data, extent

class Extraction():
    """
    SCEC CVM-H extraction.

    Init parameters
    ---------------
        2d property: 'topo', 'base', or 'moho'
        3d property: 'rho', 'vp', 'vs', or 'tag'
        3d voxet list: ['mantle', 'crust', 'lab']

    Call parameters
    ---------------
        x, y, z: sample coordinate arrays.
        out (optional): output array, same shape as x, y, and z.
        interpolation: 'nearest', 'linear'

    Returns
    -------
        f: property samples at coordinates (x, y, z)
    """
    def __init__( self, property, voxet=['mantle', 'crust', 'lab'] ):
        self.property = property
        if property in property2d:
            self.voxet = [ read_voxet( property ) ]
        else:
            self.voxet = []
            for vox in voxet:
                self.voxet += [ read_voxet( property, vox ) ]
        return
    def __call__( self, x, y, z=None, out=None, interpolation='linear' ):
        if out == None:
            out = np.empty_like( x )
            out.fill( np.nan )
        for data, extent in self.voxet:
            if self.property in property2d:
                data = data.reshape( data.shape[:2] )
                coord.interp2( extent[:2], data, (x, y), out, method=interpolation )
            else:
                coord.interp3( extent, data, (x, y, z), out, method=interpolation )
        return out

def dplane( lim, delta=500.0, property='vp', interpolation='linear' ):
    """
    Depth plane plot.
    """
    import matplotlib.pyplot as plt
    scale = 0.001
    x1, x2 = lim[0]
    y1, y2 = lim[1]
    z0 = lim[2]
    v1, v2 = lim[3]
    ex = [ scale * r for r in [x1, x2, y1, y2] ]
    x = np.arange( x1, x2 + 0.5 * delta, delta )
    y = np.arange( y1, y2 + 0.5 * delta, delta )
    y, x = np.meshgrid( y, x )
    fig = plt.figure()
    fig.clf()
    ax = plt.gca()
    m = Extraction( 'topo' )
    z = m( x, y, interpolation='linear' ) - z0
    m = Extraction( property )
    f = m( x, y, z, interpolation=interpolation )
    ax.imshow( f.T, extent=ex, vmin=v1, vmax=v2, origin='lower', interpolation='nearest' )
    ax.set_title( '%s %s' % (interpolation, property) )
    return fig

def xsection( lim, delta=(500.0, 50.0), property='vp', interpolation='linear' ):
    """
    Cross section plot.
    """
    import matplotlib.pyplot as plt
    scale = 0.001
    x1, x2 = lim[0]
    y1, y2 = lim[1]
    z1, z2 = lim[2]
    v1, v2 = lim[3]
    dx, dy = x2 - x1, y2 - y1
    L = np.sqrt( dx * dx + dy * dy )
    ex = [ scale * r for r in [0, L, z1, z2] ]
    r = np.arange( 0, L + 0.5 * delta[0], delta[0] )
    x = x1 + dx / L * r
    y = y1 + dy / L * r
    z = np.arange( z1, z2 + 0.5 * delta[1], delta[1] )
    zz, xx = np.meshgrid( z, x )
    zz, yy = np.meshgrid( z, y )
    fig = plt.figure()
    fig.clf()
    ax = plt.gca()
    m = Extraction( 'topo' )
    f = m( xx, yy, interpolation='linear' )
    ax.plot( scale*r, scale*f, 'k-' )
    m = Extraction( 'base' )
    f = m( xx, yy, interpolation='linear' )
    ax.plot( scale*r, scale*f, 'k-' )
    m = Extraction( 'moho' )
    f = m( xx, yy, interpolation='linear' )
    ax.plot( scale*r, scale*f, 'k-' )
    m = Extraction( property )
    f = m( xx, yy, zz, interpolation=interpolation )
    ax.imshow( f.T, extent=ex, vmin=v1, vmax=v2, origin='lower', interpolation='nearest' )
    ax.axis( 'auto' )
    ax.axis( ex )
    ax.set_title( '%s %s' % (interpolation, property) )
    return fig

# continue if run from the command line
if __name__ == '__main__':

    # cross sections
    delta = 100.0, 10.0
    lim = (400000.0, 400000.0), (3740000.0, 3860000.0), (-2000.0, 2000.0), (1000.0, 6000.0)
    xsection( lim, delta, 'vp', 'nearest' ).show()
    xsection( lim, delta, 'vp', 'linear' ).show()

    # depth planes
    delta = 500.0
    lim = extent[0], extent[1], 200.0, (1000.0, 6000.0)
    dplane( lim, delta, 'vp', 'nearest' ).show()
    dplane( lim, delta, 'vp', 'linear' ).show()

