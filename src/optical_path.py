'''Optical propagation'''
from numpy import cos


class OpticalPath:
    '''Path along which light propagates'''
    def __init__(self, refractive_index, thickness, ray_angle):
        self.refractive_index = refractive_index
        self.thickness = thickness
        self.ray_angle = ray_angle

    def accumulate_phase(self, free_space_wavenumber):
        '''Phase accumulated along path'''
        optical_thickness = self.refractive_index * self.thickness
        optical_path_length = 2 * optical_thickness * cos(self.ray_angle)
        return free_space_wavenumber * optical_path_length
