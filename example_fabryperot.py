import numpy as np
import matplotlib.pyplot as plt
import thinfilm as tf

# Input

n_cov = 1.0

n_in = [1.45, 3.8]
t_in = [800]

AOI = 30

lambda_0 = np.arange(500, 1000) #nm

# Calculation 

k0 = 2*np.pi/lambda_0
theta_i = AOI*tf.degrees

n_in.reverse()
t_in.reverse()

r_s = tf.next_r_s(k0, theta_i, n_cov, n_in[:], t_in[:])
r_p = tf.next_r_p(k0, theta_i, n_cov, n_in[:], t_in[:])

# Graphical output

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.set_title('Reflectance, S polarisation')
ax1.plot(lambda_0, np.abs(r_s)**2)

ax2.set_title('Reflectance, P polarisation')
ax2.plot(lambda_0, np.abs(r_p)**2)

ax2.set_xlabel('Free space wavelength (nm)')

fig.tight_layout()

fig.savefig('./example_figures/fabryperot.png')

plt.show()