'''Optical propagation'''
from numpy import cos


def accumulate_phase(wavenumber, ray_angle, thickness):
    '''Phase accumulated along path'''
    return 2 * thickness * cos(ray_angle) * wavenumber
