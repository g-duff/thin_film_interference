'''Calculate ray angles after transmission through a boundary'''
import numpy as np


def cascade_transmission_angles(incident_angle, refractive_indexes):
    '''Calculate ray angles after transmission through multiple boundary'''

    refractive_index_pairs = zip(
        refractive_indexes[:-1], refractive_indexes[1:])
    return [
        incident_angle := calculate_transmission_angle(
            coverRefractiveIndex, lowerRefractiveIndex, incident_angle
        )
        for coverRefractiveIndex, lowerRefractiveIndex in refractive_index_pairs
    ]


def calculate_transmission_angle(
    incidence_refractive_index, transmission_refractive_index, incident_angle
):
    '''Calculate a ray angle after transmission through a single boundary'''
    sin_of_transmission_angle = (
        np.sin(incident_angle) * incidence_refractive_index /
        transmission_refractive_index
    )
    angle_of_transmission = np.arcsin(sin_of_transmission_angle)
    return angle_of_transmission
