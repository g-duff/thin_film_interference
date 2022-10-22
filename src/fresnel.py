'''Fresnel reflection and transmission coefficients'''

import numpy as np


class Senkrecht:
    '''Senkrecht, or Perpendicular polarization'''
    @staticmethod
    def reflection(
        incidentAngle,
        transmissionAngle,
    ):
        '''Calculate reflection coefficient'''
        numerator = -1 * np.sin(incidentAngle - transmissionAngle)
        denominator = np.sin(incidentAngle + transmissionAngle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incidentAngle,
        transmissionAngle,
    ):
        '''Calculate transmission coefficient'''
        numerator = 2 * np.sin(transmissionAngle) * np.cos(incidentAngle)
        denominator = np.sin(incidentAngle + transmissionAngle)
        return numerator / denominator


class Parallel:
    '''Parallel polarization'''
    @staticmethod
    def reflection(
        incidentAngle,
        transmissionAngle,
    ):
        '''Calculate reflection coefficient'''
        numerator = np.tan(incidentAngle - transmissionAngle)
        denominator = np.tan(incidentAngle + transmissionAngle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incidentAngle,
        transmissionAngle,
    ):
        '''Calculate transmission coefficient'''
        numerator = 2 * np.sin(transmissionAngle) * np.cos(incidentAngle)
        denominator = np.sin(incidentAngle + transmissionAngle) * np.cos(
            incidentAngle - transmissionAngle
        )
        return numerator / denominator
