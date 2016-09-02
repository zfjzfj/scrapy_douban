#!/usr/bin/python
# -*- coding: utf8 -*-


import numpy
import matplotlib
from matplotlib import pylab, mlab, pyplot
np = numpy
plt = pyplot
from IPython.display import display
from IPython.core.pylabtools import figsize, getfigs
from pylab import *
from numpy import *


n = 10
phi = linspace(0, 2*pi)
x = cos(phi)
y = sin(phi)
for i in range(1,n):
    for j in range(1,i):
        plt.plot(x + 2 * j, y - 2 * j)

