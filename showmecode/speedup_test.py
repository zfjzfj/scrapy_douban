import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

t = np.linspace(0,10,1000)
x = signal.chirp(t,5,10,30)
plt.plot(t,x)
plt.show()
