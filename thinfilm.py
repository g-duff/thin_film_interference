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


def ellipsometry(freeSpaceWavelength, indidentAngle, refractiveIndices, thicknesses):
    """Ellipsometry parameters for an n-layer thin film stack"""

    freeSpaceWavenumber = 2 * np.pi / freeSpaceWavelength

    refractiveIndices.reverse()
    thicknesses.reverse()

    coverRefractiveIndex = refractiveIndices.pop()

    senkrechtReflection = nextLayerSenkrechtReflection(
        freeSpaceWavenumber,
        indidentAngle,
        coverRefractiveIndex,
        refractiveIndices[:],
        thicknesses[:],
    )
    parallelReflection = nextLayerParallelReflection(
        freeSpaceWavenumber,
        indidentAngle,
        coverRefractiveIndex,
        refractiveIndices[:],
        thicknesses[:],
    )

    psi, delta = reflectionToPsiDelta(senkrechtReflection, parallelReflection)

    return psi, delta


def reflectionToPsiDelta(senkrechtReflection, parallelReflection):
    """Return psi and delta ellipsometry parameters from reflection coefficients"""
    reflectionRatio = parallelReflection / senkrechtReflection
    psi = np.arctan(np.abs(reflectionRatio))
    delta = np.angle(reflectionRatio)
    return psi, delta


def nextLayerParallelReflection(
    freeSpaceWaveNumber,
    incidentAngle,
    coverRefractiveIndex,
    substrateRefractiveIndices,
    thicknesses,
):
    return nextLayerReflection(
        freeSpaceWaveNumber,
        incidentAngle,
        coverRefractiveIndex,
        substrateRefractiveIndices,
        thicknesses,
        Parallel,
    )


def nextLayerSenkrechtReflection(
    freeSpaceWaveNumber,
    incidentAngle,
    coverRefractiveIndex,
    substrateRefractiveIndices,
    thicknesses,
):
    return nextLayerReflection(
        freeSpaceWaveNumber,
        incidentAngle,
        coverRefractiveIndex,
        substrateRefractiveIndices,
        thicknesses,
        Senkrecht,
    )


def nextLayerReflection(
    freeSpaceWaveNumber,
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
        reflectionOutOf = nextLayerReflection(
            freeSpaceWaveNumber,
            transmissionAngle,
            filmRefractiveIndex,
            substrateRefractiveIndices,
            thicknesses,
            Polarization,
        )

        transmissionInto = Polarization.transmission(
            coverRefractiveIndex, filmRefractiveIndex, incidentAngle, transmissionAngle
        )
        transmissionBack = Polarization.transmission(
            filmRefractiveIndex, coverRefractiveIndex, transmissionAngle, incidentAngle
        )

        phaseDifference = calculatePhaseDifference(
            freeSpaceWaveNumber, transmissionAngle, filmRefractiveIndex, filmThickness
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


def calculatePhaseDifference(
    freeSpaceWavenumber, rayAngle, filmRefractiveIndex, filmThickness
):
    opticalThickness = filmRefractiveIndex * filmThickness
    opticalPathLength = 2 * opticalThickness * cos(rayAngle)
    return freeSpaceWavenumber * opticalPathLength


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
    """Calculates the angle of transmission at an interface"""
    sinOfAngleOfTransmission = (
        sin(incidentAngle) * incidenceRefractiveIndex / transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
