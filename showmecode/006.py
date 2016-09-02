#!/usr/bin/env python
# -*- noplot -*-

from mpl_toolkits.mplot3d import Axes3D, axes3d
import matplotlib.pyplot as plt
import numpy as np

# center and radius
center = 0
radius = 10
# data
u = np.linspace(0, 2 * np.pi, 100)
v = np.linspace(0, np.pi, 100)

ux = np.outer(np.cos(u), np.sin(v))
uy = np.outer(np.sin(u), np.sin(v))

x = radius * ux  + center
y = radius * uy + center
z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center

# plot
fig = plt.figure()
ax = fig.add_subplot(121, projection='3d')
# surface plot
ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')
# wire frame
ax = fig.add_subplot(122, projection='3d')
ax.plot_wireframe(x, y, z, rstride=4, cstride=4)
# show
plt.show()
