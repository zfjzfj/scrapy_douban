import numpy as np
import scipy as sp
import math
def mysin(x, order):
    a = x
    s = a
    for i in range(1, order):
        a *= -1 * x**2 / ((2 * i) * (2 * i + 1))
        s += a
    return s


vmysin = np.vectorize(mysin, excluded=['order'])
p = 3.141592653589793

print math.pi,sp.pi,np.pi
for i in range(1,20):
  print '%.30f' % mysin(p/2,i)

x = np.linspace(0, 2*p, 500)
y2 = vmysin(x, 2)
y3 = vmysin(x, 3)
y4 = vmysin(x, 4)
y5 = vmysin(x, 5)
y6 = vmysin(x, 6)
y7 = vmysin(x, 7)
y8 = vmysin(x, 8)
y9 = vmysin(x, 9)
y10 = vmysin(x, 10)
y = np.sin(x)

import matplotlib.pyplot as plt
plt.plot(x, y, label='sin(x)',linewidth=4)
plt.plot(x, y2, label='order 2')
plt.plot(x, y4, label='order 4')
plt.plot(x, y6, label='order 6')
plt.plot(x, y8, label='order 8')
plt.plot(x, y10, label='order 10',linewidth=2)
plt.ylim([-3, 3])
plt.legend()
plt.show()
