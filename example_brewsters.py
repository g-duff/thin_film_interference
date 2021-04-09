import numpy as np
import matplotlib.pyplot as plt
import thinfilm as tf

# Input

n_cov = 1.0
n_sub = 1.45

AOI = np.arange(0, 90)

# Constants

degrees = np.pi/180

# Calculation 

theta_i = AOI*degrees
theta_t = tf.snell_theta_t(n_cov, n_sub, theta_i)

r_s = tf.fresnel_r_s(n_cov, n_sub, theta_i, theta_t)
r_p = tf.fresnel_r_p(n_cov, n_sub, theta_i, theta_t)

# Graphical output

fig, ax = plt.subplots()

ax.plot(AOI, np.abs(r_s)**2, 'C0--', label="S polarisation")
ax.plot(AOI, np.abs(r_p)**2, 'C1--', label="P polarisation")

# ax2.set_title('Reflectance, P polarisation')
# ax2.plot(lambda_0, np.abs(r_p)**2)

# ax2.set_xlabel('Angle of indicence')

# fig.tight_layout()
plt.show()