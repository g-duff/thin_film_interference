import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import cmath

def TE(beta, d, n1, n2, n3, k0, full_output=False):

    delta = cmath.sqrt(beta**2 - (n1*k0)**2) # Top layer
    kappa = cmath.sqrt((n2*k0)**2 - beta**2) # Middle layer
    gamma = cmath.sqrt(beta**2 - (n3*k0)**2) # Bottom layer

    diff = cmath.tan(kappa*d) - kappa*(gamma+delta)/(kappa**2-gamma*delta)

    if ~full_output:
        return diff
    else:
        return delta, kappa, gamma


def TM(beta, d, n1, n2, n3, k0, full_output=False):

    delta = cmath.sqrt(beta**2 - (n1*k0)**2) # Top layer
    kappa = cmath.sqrt((n2*k0)**2 - beta**2) # Middle layer
    gamma = cmath.sqrt(beta**2 - (n3*k0)**2) # Bottom layer

    numerator = kappa*(gamma*(n2/n3)**2 + delta*(n2/n1)**2)
    denominator = kappa**2 - gamma*delta*(n2*n2/(n1*n3))**2

    diff = cmath.tan(kappa*d) - numerator/denominator

    if ~full_output:
        return diff
    else:
        return delta, kappa, gamma

lam0 = 750

n1 = 1.0
n2 = 2.1
n3 = 1.0

k0 = 2*np.pi/lam0

height = 250
width = 250

beta_in = k0*np.arange(1, 2.1, 0.01)

n_eff_TE_out = np.ones((len(beta_in)), dtype=float)
n_eff_TM_out = np.ones((len(beta_in)), dtype=float)

n_eff_TE_TM_out = np.ones((len(beta_in)), dtype=float)
n_eff_TM_TE_out = np.ones((len(beta_in)), dtype=float)


for i, b_in in enumerate(beta_in):
    print(i)

    # TE solve
    try:
        beta_out = opt.newton(TE, x0=b_in,
            args=(height, n1, n2, n3, k0), maxiter=1000, tol=1e-10)
        neff_TE = beta_out/k0
    except:
        neff_TE = 1
    n_eff_TE_out[i] = neff_TE.real

    # TM solve
    try:
        beta_out = opt.newton(TM, x0=b_in,
            args=(height, n1, n2, n3, k0), maxiter=1000, tol=1e-10)
        neff_TM = beta_out/k0
    except:
        neff_TM = 1
    n_eff_TM_out[i] = neff_TM.real

    # TE then TM solve
    try:
        beta_out = opt.newton(TE, x0=b_in,
            args=(width, n1, neff_TM.real, n3, k0), maxiter=1000, tol=1e-10)
        neff_both = beta_out/k0
    except:
        neff_both = 1
    n_eff_TE_TM_out[i] = neff_both.real


    # TM then TE solve
    try:
        beta_out = opt.newton(TM, x0=b_in,
            args=(width, n1, neff_TE.real, n3, k0), maxiter=1000, tol=1e-10)
        neff_both = beta_out/k0
    except:
        neff_both = 1
    n_eff_TM_TE_out[i] = neff_both.real


plt.hist(n_eff_TE_out, bins=110, label='TE')
plt.hist(n_eff_TM_out, bins=110, label='TM')
plt.hist(n_eff_TE_TM_out, bins=110, label='TE then TM')
plt.hist(n_eff_TM_TE_out, bins=110, label='TM then TE')


plt.legend()
plt.show()