import numpy as np
from numpy import cos, sin, exp
from Fresnel import Parallel, Senkrecht
from filmStackFactory import linkLayers

"""Library for calculating reflection from a thin film

 |
 |          Layer 1
 |
\ / incident
-------------------------------
            Layer 2
-------------------------------
            Layer 3
-------------------------------

"""

degrees = np.pi / 180


class Ellipsometer:
    def __init__(self, freeSpaceWavelength):
        self.freeSpaceWavelength = freeSpaceWavelength
        self.freeSpaceWavenumber = 2 * np.pi / freeSpaceWavelength

    def ellipsometry(self, indidentAngle, refractiveIndices, thicknesses):

        coverRefractiveIndex = refractiveIndices.pop(0)
        layers = linkLayers(refractiveIndices, thicknesses)

        senkrechtReflection = self.nextLayerReflection(
            indidentAngle,
            coverRefractiveIndex,
            layers,
            Senkrecht,
        )
        parallelReflection = self.nextLayerReflection(
            indidentAngle,
            coverRefractiveIndex,
            layers,
            Parallel,
        )

        return reflectionToPsiDelta(senkrechtReflection, parallelReflection)

    def nextLayerReflection(
        self,
        incidentAngle,
        coverRefractiveIndex,
        layers,
        Polarization,
    ):
        toRefractiveIndex = layers.refractiveIndex
        transmissionAngle = calculateTransmissionAngle(
            coverRefractiveIndex, toRefractiveIndex, incidentAngle
        )
        reflectionInto = Polarization.reflection(
            coverRefractiveIndex, toRefractiveIndex, incidentAngle, transmissionAngle
        )

        if layers.hasNextLayer():
            reflectionOutOf = self.nextLayerReflection(
                transmissionAngle,
                layers.refractiveIndex,
                layers.nextLayer,
                Polarization,
            )

            transmissionInto = Polarization.transmission(
                coverRefractiveIndex,
                toRefractiveIndex,
                incidentAngle,
                transmissionAngle,
            )
            transmissionBack = Polarization.transmission(
                toRefractiveIndex,
                coverRefractiveIndex,
                transmissionAngle,
                incidentAngle,
            )

            phaseDifference = self.calculatePhaseDifference(
                transmissionAngle, toRefractiveIndex, layers.thickness
            )

            reflectionInto = calculateFilmReflection(
                phaseDifference,
                reflectionInto,
                reflectionOutOf,
                transmissionInto,
                transmissionBack,
            )

        return reflectionInto

    def calculatePhaseDifference(self, rayAngle, filmRefractiveIndex, filmThickness):
        opticalThickness = filmRefractiveIndex * filmThickness
        opticalPathLength = 2 * opticalThickness * cos(rayAngle)
        return self.freeSpaceWavenumber * opticalPathLength


def reflectionToPsiDelta(senkrechtReflection, parallelReflection):
    reflectionRatio = parallelReflection / senkrechtReflection
    psi = np.arctan(np.abs(reflectionRatio))
    delta = np.angle(reflectionRatio)
    return psi, delta


def calculateFilmReflection(
    accumulatedPhase,
    reflectionInto,
    reflectionOutOf,
    transmissionInto,
    transmissionBack,
):
    numerator = transmissionInto * reflectionOutOf * transmissionBack
    demoninator = exp(-1j * accumulatedPhase) + reflectionInto * reflectionOutOf
    return reflectionInto + numerator / demoninator


def calculateTransmissionAngle(
    incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle
):
    sinOfAngleOfTransmission = (
        sin(incidentAngle) * incidenceRefractiveIndex / transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
