import numpy as np
import matplotlib.pyplot as plt
import thinfilm as tf

# Input

n_cov = 1.0

n_in = [3.8, 1.45, 3.8]
t_in = [220, 3000]

AOI = 65

lambda_0 = np.arange(500, 1000) #nm

# Calculation 

k0 = 2*np.pi/lambda_0
theta_i = AOI*tf.degrees

n_in.reverse()
t_in.reverse()

r_s = tf.next_r_s(k0, theta_i, n_cov, n_in[:], t_in[:])
r_p = tf.next_r_p(k0, theta_i, n_cov, n_in[:], t_in[:])

psi, delta = tf.psi_delta(r_s, r_p)

# Graphical output

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.set_title(r'tan$(\Psi$)')
ax1.plot(lambda_0, np.tan(psi))

ax2.set_title(r'cos$(\Delta$)')
ax2.plot(lambda_0, np.cos(delta))

ax2.set_xlabel('Free space wavelength (nm)')

fig.tight_layout()
plt.show()