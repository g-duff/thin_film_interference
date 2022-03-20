import numpy as np
from numpy import cos, sin, exp
from Fresnel import Parallel, Senkrecht

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

        refractiveIndices.reverse()
        thicknesses.reverse()

        coverRefractiveIndex = refractiveIndices.pop()

        senkrechtReflection = self.nextLayerReflection(
            indidentAngle,
            coverRefractiveIndex,
            refractiveIndices[:],
            thicknesses[:],
            Senkrecht,
        )
        parallelReflection = self.nextLayerReflection(
            indidentAngle,
            coverRefractiveIndex,
            refractiveIndices[:],
            thicknesses[:],
            Parallel,
        )

        psi, delta = reflectionToPsiDelta(senkrechtReflection, parallelReflection)

        return psi, delta

    def nextLayerReflection(
        self,
        incidentAngle,
        coverRefractiveIndex,
        substrateRefractiveIndices,
        thicknesses,
        Polarization,
    ):
        # Base quantities
        filmRefractiveIndex = substrateRefractiveIndices.pop()
        transmissionAngle = calculateTransmissionAngle(
            coverRefractiveIndex, filmRefractiveIndex, incidentAngle
        )
        reflectionInto = Polarization.reflection(
            coverRefractiveIndex, filmRefractiveIndex, incidentAngle, transmissionAngle
        )

        try:
            # Interference inside a thin film, calculated using
            # a Fabry-Perot model
            filmThickness = thicknesses.pop()
            reflectionOutOf = self.nextLayerReflection(
                transmissionAngle,
                filmRefractiveIndex,
                substrateRefractiveIndices,
                thicknesses,
                Polarization,
            )

            transmissionInto = Polarization.transmission(
                coverRefractiveIndex,
                filmRefractiveIndex,
                incidentAngle,
                transmissionAngle,
            )
            transmissionBack = Polarization.transmission(
                filmRefractiveIndex,
                coverRefractiveIndex,
                transmissionAngle,
                incidentAngle,
            )

            phaseDifference = self.calculatePhaseDifference(
                transmissionAngle,
                filmRefractiveIndex,
                filmThickness,
            )

            reflectionInto = calculateFilmReflection(
                phaseDifference,
                reflectionInto,
                reflectionOutOf,
                transmissionInto,
                transmissionBack,
            )

        except IndexError:
            # Reflectance for a single interface when
            # no finite thicknesses are left in the stack
            pass

        finally:
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
