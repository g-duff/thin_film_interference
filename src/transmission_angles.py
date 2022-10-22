'''Calculate ray angles after transmission through a boundary'''
import numpy as np


def propagate_transmission_angles(incidentAngle, refractiveIndexPairs):
    '''Calculate ray angles after transmission through multiple boundary'''
    return [
        incidentAngle := calculate_transmission_angle(
            coverRefractiveIndex, lowerRefractiveIndex, incidentAngle
        )
        for coverRefractiveIndex, lowerRefractiveIndex in refractiveIndexPairs
    ]


def calculate_transmission_angle(
    incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle
):
    '''Calculate a ray angle after transmission through a single boundary'''
    sinOfAngleOfTransmission = (
        np.sin(incidentAngle) * incidenceRefractiveIndex /
        transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
