import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import cmath
import functools as ftl

def field_coefficients(beta, n1, n2, n3, k0):
    '''For a 3-layer slab waveguide'''

    delta = cmath.sqrt(beta**2 - (n3*k0)**2) # Top layer
    kappa = cmath.sqrt((n2*k0)**2 - beta**2) # Middle layer
    gamma = cmath.sqrt(beta**2 - (n1*k0)**2) # Bottom layer

    return delta, kappa, gamma


def three_layers(beta, d, n1, n2, n3, k0):

    delta, kappa, gamma = field_coefficients(beta, n1, n2, n3, k0)
    diff = cmath.tan(kappa*d) - kappa*(gamma+delta)/(kappa**2-gamma*delta)

    return diff


def three_layer_TE(beta, d, n1, n2, n3, k0):
    ''' '''

    delta, kappa, gamma = field_coefficients(beta, n1, n2, n3, k0)
    diff = cmath.tan(kappa*d) - kappa*(gamma+delta)/(kappa**2-gamma*delta)

    return diff


def three_layer_TM(beta, d, n1, n2, n3, k0):

    field_coefficients(beta, n1, n2, n3, k0)

    numerator = kappa*(gamma*(n2/n3)**2 + delta*(n2/n1)**2)
    denominator = kappa**2 - gamma*delta*(n2*n2/(n1*n3))**2

    diff = cmath.tan(kappa*d) - numerator/denominator

    return diff

def n_layers(beta, d, n, k0):

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

def multilayer_opt(beta, d, n, k0):
    '''Based on the physics of sec 5.2.3 Slab Waveguide
    Models an n-layer slab waveguide. 
    Minimize to find guided modes.

    Inputs
    beta: propagation constant, float
    d: layer thickesses, 1D iterable of floats
    n: layer RI, iterable of floats same length as d 
    k0: wave vector in free space

    Outputs:
    diff: float
    '''
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
