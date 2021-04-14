import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import cmath


def general_matrix(beta, d, n, k0):

    kx = [cmath.sqrt((k0*ni)**2 - beta**2) for ni in n]
    alpha = [1j*kxi for kxi in kx]
    delta_p_1 = [a*di for a, di in zip(alpha[1:], d[1:])]  # Delta plus one

    matrices = [np.array([[(a+a_p1)*np.exp(-d_p1), (a-a_p1)*np.exp(d_p1)],
                          [(a-a_p1)*np.exp(-d_p1), (a+a_p1)*np.exp(d_p1)]]
                         )/(2*a) for a, a_p1, d_p1 in zip(alpha, alpha[1:], delta_p_1)]

    M = matrices[0]
    for m in matrices[1:]:
        M = M@m
    diff = M[0, 0]

    return diff


def three_layers(beta, d, n1, n2, n3, k0, full_output=False):

    delta = cmath.sqrt(beta**2 - (n3*k0)**2)
    kappa = cmath.sqrt((n2*k0)**2 - beta**2)
    gamma = cmath.sqrt(beta**2 - (n1*k0)**2)

    diff = cmath.tan(kappa*d) - kappa*(gamma+delta)/(kappa**2-gamma*delta)

    if ~full_output:
        return diff
    else:
        return diff, delta, kappa, gamma


lam0 = 1550
k0 = 2*np.pi/lam0
beta_in = k0*np.arange(1.5, 2.1, 0.01)
mid_thickness = np.arange(750, 1501, 25)

n = [1.0, 2.1, 1.5]

three_layer_out = np.ones((len(mid_thickness), len(beta_in)), dtype=np.complex)
matrix_out = np.ones((len(mid_thickness), len(beta_in)), dtype=np.complex)

for i, t in enumerate(mid_thickness):
    for j, b_in in enumerate(beta_in):
        three_layer_out[i,j] = three_layers(b_in, t, n[1-1], n[2-1], n[3-1], k0)
        matrix_out[i,j] = general_matrix(b_in, [0,t,0], n, k0)


fix, (ax1, ax2) = plt.subplots(ncols=2)
ax1.pcolormesh(abs(three_layer_out))
ax2.pcolormesh(abs(matrix_out))

plt.show()
