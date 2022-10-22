'''Calculate ray angles after transmission through a boundary'''
import numpy as np


def propagateTransmissionAngles(incidentAngle, refractiveIndexPairs):
    '''Calculate ray angles after transmission through multiple boundary'''
    return [
        incidentAngle := calculateTransmissionAngle(
            coverRefractiveIndex, lowerRefractiveIndex, incidentAngle
        )
        for coverRefractiveIndex, lowerRefractiveIndex in refractiveIndexPairs
    ]


def calculateTransmissionAngle(
    incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle
):
    '''Calculate a ray angle after transmission through a single boundary'''
    sinOfAngleOfTransmission = (
        np.sin(incidentAngle) * incidenceRefractiveIndex /
        transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
