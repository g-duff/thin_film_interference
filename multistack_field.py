import matplotlib.pyplot as plt
import matplotlib.gridspec as gsp
import numpy as np
import cmath
import scipy.optimize as opt
import functools as ftl
 
def multilayer_opt(beta, d, n, k0):

    kx = [cmath.sqrt((k0*ni)**2 - beta**2) for ni in n]
    alpha = [1j*kxi for kxi in kx]
    delta_p_1 = [a*di for a, di in zip(alpha[1:], d[1:])]  # Delta plus one

    matrices = [np.array([[(a+a_p1)*np.exp(-d_p1), (a-a_p1)*np.exp(d_p1)],
                        [(a-a_p1)*np.exp(-d_p1), (a+a_p1)*np.exp(d_p1)]]
    )/(2*a) for a, a_p1, d_p1 in zip(alpha, alpha[1:], delta_p_1)]

    M = ftl.reduce(np.matmul, matrices)
    diff = M[0,0]

    return abs(diff)


def multilayer_field(beta, d, n, k0):

    kx = [cmath.sqrt((k0*ni)**2 - beta**2) for ni in n]

    alpha = [1j*kxi for kxi in kx]
    delta_p_1 = [a*di for a, di in zip(alpha[1:], d[1:])]  # Delta plus one

    matrices = [np.array([[(a+a_p1)*cmath.exp(-d_p1), (a-a_p1)*cmath.exp(d_p1)],
                          [(a-a_p1)*cmath.exp(-d_p1), (a+a_p1)*cmath.exp(d_p1)]]
    )/(2*a) for a, a_p1, d_p1 in zip(alpha, alpha[1:], delta_p_1)]

    ab = np.array([1, 0])
    AB = []
    AB.append(ab)
    for m in matrices[::-1]:
        ab = m@ab
        AB.append(ab)
    A, B = np.array(AB[::-1]).T

    return np.array(kx), A, B


def e_field(x, A, B, kxx, aa):
    y = A*np.exp(1j*kxx*(x-aa)) + B*np.exp(-1j*kxx*(x-aa))
    return y


lam0 = 750

N = [1.45, 2.02, 1.66, 1.06, 1.45]
a = np.array([0, 400, 495, 500, 1000])

k0 = 2*np.pi/lam0
beta_in = k0*1.7

t = [0] + list(a[1:] - a[:-1])

try:
    beta_out = opt.newton(multilayer_opt, x0=beta_in,
    args=(t, N, k0), maxiter=100, tol=1e-10)
except:
    beta_out = k0
    print('Solver failed')

print(f'Effective index: {beta_out/k0}')

kx, Aout, Bout = multilayer_field(beta_out, t, N, k0)

ai = [-1000] + list(a)
X = [np.arange(xi, xf) for xi, xf in zip(ai, a)]
E = [e_field(*params) for params in zip(X, Aout, Bout, kx, a)]


grid = gsp.GridSpec(nrows=4, ncols=1)

fig = plt.figure()
ax2 = fig.add_subplot(grid[3:])
ax1 = fig.add_subplot(grid[:3])


for x, e, n in zip(X, E, N):
    ax1.plot(x, e.real)

RI = [np.ones(x.shape)*n for x, n in zip(X, N)]
x = np.concatenate(X)
RI = np.concatenate(RI)
ax2.plot(x, RI, color='k')

for ai in a[:-1]:
    ax1.axvline(ai, color='k', ls='--')

ax1.set_ylabel('E field amplitude')
ax2.set_ylabel('Ref index')

ax1.set_xticks([])
ax2.set_xlabel('x (nm)')

plt.show()
