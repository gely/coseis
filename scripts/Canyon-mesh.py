#!/usr/bin/env python
"""
2d Semicircular canyon mesh
"""
import os
import math
import numpy as np
import matplotlib.pyplot as plt

# parameters
L = 11.0
r0 = 1.0
n1, n2 = 301, 321

# step sizes
n = (n2 - 1) / 2
dy0 = 0.5 * math.pi * r0 / (n2 - 1)
dy1 = L / n

# semicircle canyon
f = np.linspace(0.0, 0.5 * math.pi, n2)
x = np.empty([n1, n2])
y = np.empty([n1, n2])
x[0, :] = np.cos(f) * r0
y[0, :] = np.sin(f) * r0

# outer edge
x[-1, :] = L
x[-1, -n:] = np.arange(n)[::-1] * dy1
y[-1, :] = L
y[-1, :n] = np.arange(n) * dy1

# blend
w = np.cumsum(np.linspace(2.0 * dy0, dy1, n1 - 1))
w = w / w[-1]
for i in range(1, n1-1):
    x[i, :] = (1.0 - w[i-1]) * x[0, :] + w[i-1] * x[-1, :]
    y[i, :] = (1.0 - w[i-1]) * y[0, :] + w[i-1] * y[-1, :]

# print mesh properties
vp = 2.0
dy = y[0, 1] - y[0, 0]
dt = dy * 1.5 / vp / math.sqrt(3.0)
print('shape = ', (n1, n2))
print('nt > ', L / vp / dt)
print('dt < ', dt)
print('L = ', L)
print('L / n = ', L / n)
print('dx00 = ', (x[1, 0] - x[0, 0],     y[0, 1] - y[0, 0]))
print('dx01 = ', (x[0, -2] - x[0, -1],   y[1, -1] - y[0, -1]))
print('dx10 = ', (x[-1, 0] - x[-2, 0],   y[-1, 1] - y[-1, 0]))
print('dx11 = ', (x[-1, -2] - x[-1, -1], y[-1, -1] - y[-2, -1]))

# write files
p = 'repo/Canyon'
os.mkdir(p)
os.chdir(p)
x.T.astype('f').tofile('x.bin')
y.T.astype('f').tofile('y.bin')

# plot
fig = plt.gcf()
fig.clf()
ax = fig.add_subplot(111)
d = 10
x, y = x[::d, ::d], y[::d, ::d]
ax.plot(x, y, 'k-')
ax.plot(-x, y, 'k-')
ax.plot(x.T, y.T, 'k-')
ax.plot(-x.T, y.T, 'k-')
ax.axis('scaled')
ax.axis([-2, 2, 2, -0.2])
fig.savefig('Canyon-Mesh.svg')
fig.show()
