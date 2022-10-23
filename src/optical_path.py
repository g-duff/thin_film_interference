'''Optical propagation'''
import numpy as np


def accumulate_phase(free_space_wavenumber, ray_angle, refractive_index, thickness):
    '''Phase accumulated along path'''
    optical_path_difference = 2 * refractive_index * \
        thickness * np.cos(ray_angle)
    return optical_path_difference * free_space_wavenumber
