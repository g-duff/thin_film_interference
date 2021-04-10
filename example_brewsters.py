import numpy as np
import matplotlib.pyplot as plt
import thinfilm as tf

# Input

n_cov = 1.0
n_sub = 1.45

AOI = np.arange(0, 90)

# Calculation 

theta_i = AOI*tf.degrees
theta_t = tf.snell_theta_t(n_cov, n_sub, theta_i)

r_s = tf.fresnel_r_s(n_cov, n_sub, theta_i, theta_t)
r_p = tf.fresnel_r_p(n_cov, n_sub, theta_i, theta_t)

# Graphical output

fig, ax = plt.subplots()

ax.plot(AOI, np.abs(r_s)**2, 'C0--', label="S polarisation")
ax.plot(AOI, np.abs(r_p)**2, 'C3--', label="P polarisation")

ax.set_xlabel('Angle of incidence (degrees)')
ax.set_ylabel('Reflectance')
ax.legend()

fig.savefig('./example_figures/brewsters.png')

plt.show()