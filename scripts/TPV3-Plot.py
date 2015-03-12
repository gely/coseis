#!/usr/bin/env python
import os, json, glob
import numpy as np
import matplotlib.pyplot as plt

# parameters
stations = 'P1a', 'P2a'
stations = 'P1b', 'P2b'
stations = 'P1', 'P2'
bipath = 'bi/'
runs = 'run/tpv3-*'

# loop over runs
for path in glob.glob(runs):

    # metadata
    path += os.sep
    meta = json.load(open(path + 'meta.json'))
    shape = meta['shape']
    delta = meta['delta']
    hypo  = meta['hypocenter']
    dtype = meta['dtype']

    # time histories
    t1 = np.arange(shape[-1]) * delta[-1]
    t2 = np.load(bipath + 'TPV3-BI-Time.npy')

    # loop over stations
    for i, sta in enumerate(stations):
        fig = plt.figure(i+1)
        fig.clf()

        # shear stress
        ax = fig.add_subplot(2, 1, 1)
        f1 = np.fromfile(path + sta + '-ts1.bin', dtype) * 1e-6
        f2 = np.load(bipath + 'TPV3-BI-' + sta[:2] + '-Traction.npy')
        ax.plot(t1, f1, 'k-', t2, f2, 'k--')
        ax.axis([1, 11, 60, 85])
        ax.set_title(sta, position=(0.05, 0.83), ha='left', va='center')
        ax.set_xticklabels([])
        ax.set_ylabel('Shear stress (MPa)')
        #leg = fig.legend(('SOM', 'BI'), loc=(0.78, 0.6))

        # slip rate
        ax = fig.add_subplot(2, 1, 2)
        f1 = np.fromfile(path + sta + '-sv1.bin', dtype)
        f2 = np.load(bipath + 'TPV3-BI-' + sta[:2] + '-Slip-Rate.npy')
        ax.plot(t1, f1, 'k-', t2, f2, 'k--')
        ax.set_yticks([0, 1, 2, 3])
        ax.set_ylabel('Slip rate (m/s)')

        # slip
        ax.twinx()
        f1 = np.fromfile(path + sta + '-su1.bin', dtype)
        f2 = np.load(bipath + 'TPV3-BI-' + sta[:2] + '-Slip.bin')
        ax.plot(t1, f1, 'k-', t2, f2, 'k--')
        ax.axis([1, 11, -0.5, 3.5])
        ax.set_yticks([0, 1, 2, 3])
        ax.set_ylabel('Slip (m)')
        ax.set_xlabel('Time (s)')

        # finish up
        ax.set_title(sta, position=(0.05, 0.83), ha='left', va='center')
        fig.canvas.draw()
        f = path + 'tpv3-%03d-%s' % (delta[0], sta)
        print f
        fig.savefig(f + '.png')
        fig.savefig(f + '.pdf')

    # Rupture time contour
    fig = plt.figure(3)
    fig.clf()
    ax = fig.add_subplot(111)
    v = np.arange(-20, 20) * 0.5

    # SOM
    n = meta['shapes']['trup.bin']
    x = np.fromfile(path + 'x1.bin', dtype).reshape(n[::-1]).T
    y = np.fromfile(path + 'x2.bin', dtype).reshape(n[::-1]).T
    t = np.fromfile(path + 'trup.bin', dtype).reshape(n[::-1]).T
    if 'fixhypo' not in meta:
        x = x - delta[0] * (hypo[0] - 1)
        y = y - delta[1] * (hypo[1] - 1)
    x *= 0.001
    y *= 0.001
    ax.contour(x, y, t, v, colors='k')

    # BI
    t = np.load(bipath + 'TPV3-BI-Rupture-Time.npy')
    n = t.shape
    dx = 0.1
    x = dx * np.arange(n[0])
    y = dx * np.arange(n[1])
    x -= 0.5 * x[-1]
    y -= 0.5 * y[-1]
    y, x = np.meshgrid(y, x)
    ax.contour(x, y, -t, v, colors='k')

    # finish up
    ax.axis('image')
    ax.axis([-15, 0, -7.5, 0])
    fig.canvas.draw()
    f = path + 'TPV3-%03d-trup' % delta[0]
    print f
    fig.savefig(f + '.png')
    fig.savefig(f + '.pdf')
    fig.show()
