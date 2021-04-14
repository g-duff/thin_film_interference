import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import cmath
import waveguide as wg

lam0 = 750

n1 = 1.0
n2 = 2.1
n3 = 1.5

k0 = 2*np.pi/lam0

t = 500
beta_in = k0*1.89

print(f'Solving {t:2.1f} nm')
try:
    beta_out = opt.newton(wg.three_layer_TE, x0=beta_in,
    args=(t, n1, n2, n3, k0), maxiter=1000, tol=1e-12)
except:
    beta_out = k0
    print('Solver failed')


neff = beta_out/k0
print(f'Effective refractive index: {neff}')

(delta, kappa, gamma) = (wg.field_coefficients(beta_out, n1, n2, n3, k0))

A = 1
B = -delta/kappa

x1 = np.arange(0, t, 1)
x2 = np.arange(-t, 0, 1)
x3 = np.arange(-2*t, -t, 1)

e1 = A*np.exp(-delta*x1)
e2 = A*np.cos(kappa*x2) + B*np.sin(kappa*x2)
e3 = (A*np.cos(kappa*t) - B*np.sin(kappa*t))*np.exp(gamma*(x3+t))

fig, ax = plt.subplots()
ax.plot(x1, e1.real)
ax.plot(x2, e2.real)
ax.plot(x3, e3.real)
plt.show()
