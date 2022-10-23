'''Fresnel reflection and transmission coefficients'''

import numpy as np


class Senkrecht:
    '''Senkrecht, or Perpendicular polarization'''
    @staticmethod
    def reflection(
        incident_wavevector_normal_component,
        transmission_wavevector_normal_component,
    ):
        '''Calculate reflection coefficient'''
        numerator = incident_wavevector_normal_component - \
            transmission_wavevector_normal_component
        denominator = incident_wavevector_normal_component + \
            transmission_wavevector_normal_component
        return numerator / denominator

    @staticmethod
    def transmission(
        incident_wavevector_normal_component,
        transmission_wavevector_normal_component,
    ):
        '''Calculate transmission coefficient'''
        numerator = 2 * incident_wavevector_normal_component
        denominator = incident_wavevector_normal_component + \
            transmission_wavevector_normal_component
        return numerator / denominator


class Parallel:
    '''Parallel polarization'''
    @staticmethod
    def reflection(
        incident_angle,
        transmission_angle,
    ):
        '''Calculate reflection coefficient'''
        numerator = np.tan(incident_angle - transmission_angle)
        denominator = np.tan(incident_angle + transmission_angle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incident_angle,
        transmission_angle,
    ):
        '''Calculate transmission coefficient'''
        numerator = 2 * np.sin(transmission_angle) * np.cos(incident_angle)
        denominator = np.sin(incident_angle + transmission_angle) * np.cos(
            incident_angle - transmission_angle
        )
        return numerator / denominator
