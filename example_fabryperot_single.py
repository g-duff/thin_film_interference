import numpy as np
import matplotlib.pyplot as plt
import thinfilm as tf

# Input

n_cov = 1.0
n_film = 1.45
n_subs = 3.8

t_film = 800

AOI = 30

lambda_0 = np.arange(500, 1000)  # nm

# Angles

theta_i = AOI*tf.degrees                            # incident
theta_f = tf.calculateAngleOfTransmission(n_cov, n_film, theta_i)  # film
theta_t = tf.calculateAngleOfTransmission(n_film, n_subs, theta_f)  # transmitted

# Fresnel coefficients for both polarisations

fresnel_s = {
    'r12': tf.calculateSenkrechtReflection(n_cov, n_film, theta_i, theta_f),
    'r23': tf.calculateSenkrechtReflection(n_film, n_subs, theta_f, theta_t),
    't12': tf.calculateSenkrechtTransmission(n_cov, n_film, theta_i, theta_f),
    't21': tf.calculateSenkrechtTransmission(n_film, n_cov, theta_f, theta_i),
}

fresnel_p = {
    'r12': tf.calculateParallelReflection(n_cov, n_film, theta_i, theta_f),
    'r23': tf.calculateParallelReflection(n_film, n_subs, theta_f, theta_t),
    't12': tf.calculateParallelTransmission(n_cov, n_film, theta_i, theta_f),
    't21': tf.calculateParallelTransmission(n_film, n_cov, theta_f, theta_i),
}

# Phase difference from rays

k0 = 2*np.pi/lambda_0
delta = tf.calculatePhaseDifference(k0, n_film, t_film, theta_f)

# Multiple beam interference in Fabry Perot cavity

r_s = tf.fabry_perot_refl(delta,  **fresnel_s)
r_p = tf.fabry_perot_refl(delta,  **fresnel_p)

# Graphical output

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.set_title('S polarisation')
ax1.set_ylabel('Reflectance')
ax1.plot(lambda_0, np.abs(r_s)**2)

ax2.set_title('P polarisation')
ax2.set_ylabel('Reflectance')
ax2.plot(lambda_0, np.abs(r_p)**2)

ax2.set_xlabel('Free space wavelength (nm)')

fig.tight_layout()

fig.savefig('./example_figures/fabryperot_single.png')

plt.show()
