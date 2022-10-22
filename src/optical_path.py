'''Optical propagation'''
from numpy import cos

def accumulate_phase(wavenumber, ray_angle, thickness):
    '''Phase accumulated along path'''
    optical_path_length = thickness * cos(ray_angle) * wavenumber
    return optical_path_length
