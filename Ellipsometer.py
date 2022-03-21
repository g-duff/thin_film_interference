import numpy as np
from numpy import cos, sin, exp
from Fresnel import Parallel, Senkrecht
from filmStackFactory import linkRefractiveIndices, linkThicknesses

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

        refractiveIndices = linkRefractiveIndices(refractiveIndices)
        thicknesses = linkThicknesses(thicknesses)

        senkrechtReflection = self.nextLayerReflection(
            indidentAngle,
            refractiveIndices,
            thicknesses,
            Senkrecht,
        )
        parallelReflection = self.nextLayerReflection(
            indidentAngle,
            refractiveIndices,
            thicknesses,
            Parallel,
        )

        return reflectionToPsiDelta(senkrechtReflection, parallelReflection)

    def nextLayerReflection(
        self,
        incidentAngle,
        refractiveIndices,
        thicknesses,
        Polarization,
    ):
        # Base quantities
        fromRefractiveIndex = refractiveIndices.thisValue
        toRefractiveIndex = refractiveIndices.nextValue.thisValue
        transmissionAngle = calculateTransmissionAngle(
            fromRefractiveIndex, toRefractiveIndex, incidentAngle
        )
        reflectionInto = Polarization.reflection(
            fromRefractiveIndex, toRefractiveIndex, incidentAngle, transmissionAngle
        )

        if thicknesses is not None:
            # Interference inside a thin film, calculated using
            # a Fabry-Perot model
            reflectionOutOf = self.nextLayerReflection(
                transmissionAngle,
                refractiveIndices.nextValue,
                thicknesses.nextValue,
                Polarization,
            )

            transmissionInto = Polarization.transmission(
                fromRefractiveIndex,
                toRefractiveIndex,
                incidentAngle,
                transmissionAngle,
            )
            transmissionBack = Polarization.transmission(
                toRefractiveIndex,
                fromRefractiveIndex,
                transmissionAngle,
                incidentAngle,
            )

            phaseDifference = self.calculatePhaseDifference(
                transmissionAngle,
                toRefractiveIndex,
                thicknesses.thisValue
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
    accumulatedPhase = exp(-1j * accumulatedPhase)
    numerator = transmissionInto * reflectionOutOf * transmissionBack
    demoninator = accumulatedPhase + reflectionInto * reflectionOutOf
    return reflectionInto + numerator / demoninator


def calculateTransmissionAngle(
    incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle
):
    sinOfAngleOfTransmission = (
        sin(incidentAngle) * incidenceRefractiveIndex / transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
