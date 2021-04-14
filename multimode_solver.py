import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import cmath

# Needs actually implementing


def three_layers(beta, d, n1, n2, n3, k0, full_output=False):

    delta = cmath.sqrt(beta**2 - (n3*k0)**2)
    kappa = cmath.sqrt((n2*k0)**2 - beta**2)
    gamma = cmath.sqrt(beta**2 - (n1*k0)**2)

    diff = cmath.tan(kappa*d) - kappa*(gamma+delta)/(kappa**2-gamma*delta)

    if ~full_output:
        return diff
    else:
        return delta, kappa, gamma

lam0 = 1550

n1 = 1.0
n2 = 2.1
n3 = 1.5

k0 = 2*np.pi/lam0
beta_in = k0*np.arange(n3, n2, 0.01)

thicknesses = np.arange(750, 1501, 25)
neff = np.ones((len(thicknesses), len(beta_in)), dtype=np.complex)

for i, t in enumerate(thicknesses):
    print(f'Solving {t:2.1f} nm')
    for j, b_in in enumerate(beta_in):
        try:
            beta_out = opt.newton(three_layers, x0=b_in,
                args=(t, n1, n2, n3, k0), maxiter=100, tol=1e-7)
        except:
            beta_out = k0
        neff[i, j] = beta_out/k0

fig, ax = plt.subplots()

for ne in neff.T:
    ax.plot(thicknesses, ne.real, 'ko', ms=1)

ax.set_ylim([n3, n2])
ax.set_xlabel('Guide thickness (nm)')
ax.set_ylabel(r'$n_{eff}$')
plt.show()
