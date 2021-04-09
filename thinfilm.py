import numpy as np
from numpy import cos, sin, exp
import cmath

'''Library for calculating reflection from a thin film

 |
 |          Layer 1
 |
\ / incident
-------------------------------
            Layer 2
-------------------------------
            Layer 3
-------------------------------

'''

# Constants

degrees = np.pi/180

def snell_theta_t(n1, n2, theta_1):
    '''Calculates the angle of transmission at an interface'''
    sintheta_2 = sin(theta_1)*n1/n2
    theta_2 = np.arcsin(sintheta_2)
    return theta_2


def fresnel_r_s(n1, n2, theta_i, theta_t):
    ''' Fresnel reflection coefficient
    Senkrecht polarisation'''
    rs = (n1*cos(theta_i)-n2*cos(theta_t))/(n1*cos(theta_i)+n2*cos(theta_t))
    return rs


def fresnel_t_s(n1, n2, theta_i, theta_t):
    ''' Fresnel transmission coefficient
    Senkrecht polarization'''
    ts = 2*n1*cos(theta_i)/(n1*cos(theta_i) + n2*cos(theta_t))
    return ts


def fresnel_r_p(n1, n2, theta_i, theta_t):
    ''' Fresnel reflection coefficient
    Parallel polarisation'''
    rp = (n2*cos(theta_i)-n1*cos(theta_t))/(n2*cos(theta_i)+n1*cos(theta_t))
    return rp


def fresnel_t_p(n1, n2, theta_i, theta_t):
    ''' Fresnel transmission coefficient
    Parallel polarisation'''
    tp = 2*n1*cos(theta_i)/(n2*cos(theta_i) + n1*cos(theta_t))
    return tp


def phase_difference(k0, nf, d, theta_t):
    ''' The phase difference 
    between two parallel rays reflected at thin film interfaces'''
    L = 2*nf*d*cos(theta_t)
    pd = k0 * L
    return pd


def fabry_perot_refl(delta, r12, r23, t12, t21):
    ''' Fabry Perot reflection coefficient '''  
    phase_term = exp(-1j*delta)
    r = r12 + t12*r23*t21/(phase_term+r12*r23)
    return r


def psi_delta(r_s, r_p):
    '''Return psi and delta ellipsometry parameters from reflection coefficients'''
    rho = r_p/r_s
    p = np.arctan(np.abs(rho))
    d = d = np.angle(rho)
    return p, d


def next_r_s(k0, theta_i, n_cov, n_sub, thicknesses=None):
    ''' Return reflection for the next layer 
    Senkrecht polarisation'''

    # Base quantities    
    n_film = n_sub.pop()
    theta_t = snell_theta_t(n_cov, n_film, theta_i)
    r12 = fresnel_r_s(n_cov, n_film, theta_i, theta_t)

    try:
        # Interference inside a thin film, calculated using 
        # a Fabry-Perot model 
        t = thicknesses.pop()
        r23 = next_r_s(k0, theta_t, n_film, n_sub, thicknesses)

        t12 = fresnel_t_s(n_cov, n_film, theta_i, theta_t)
        t21 = fresnel_t_s(n_film, n_cov, theta_t, theta_i)

        delta = phase_difference(k0, n_film, t, theta_t)
        phase_term = exp(-1j*delta)

        r = fabry_perot_refl(delta, r12, r23, t12, t21)

    except IndexError:
        # Reflectance for a single interface when  
        # no finite thicknesses are left in the stack
        r = r12
    
    finally:
        return r


def next_r_p(k0, theta_i, n_cov, n_sub, thicknesses=None):
    ''' Return reflection for the next layer 
    Parallel  polarisation'''
    
    # Base quantities    
    n_film = n_sub.pop()
    theta_t = snell_theta_t(n_cov, n_film, theta_i)
    r12 = fresnel_r_p(n_cov, n_film, theta_i, theta_t)

    try:
        # Interference inside a thin film, calculated using
        # a Fabry-Perot model 
        t = thicknesses.pop()
        r23 = next_r_p(k0, theta_t, n_film, n_sub, thicknesses)

        t12 = fresnel_t_p(n_cov, n_film, theta_i, theta_t)
        t21 = fresnel_t_p(n_film, n_cov, theta_t, theta_i)

        delta = phase_difference(k0, n_film, t, theta_t)
        phase_term = exp(-1j*delta)

        r = fabry_perot_refl(delta, r12, r23, t12, t21)

    except IndexError:
        # Reflectance for a single interface when  
        # no finite thicknesses are left in the stack
        r = r12

    finally:
        return r