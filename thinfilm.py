import numpy as np
from numpy import cos, sin, exp

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
    """Return reflection for the next layer
    Parallel  polarisation"""
    return nextLayerReflection(
        freeSpaceWaveNumber,
        incidentAngle,
        coverRefractiveIndex,
        substrateRefractiveIndices,
        thicknesses,
        calculateParallelTransmission,
        calculateParallelReflection,
    )


def nextLayerSenkrechtReflection(
    freeSpaceWaveNumber,
    incidentAngle,
    coverRefractiveIndex,
    substrateRefractiveIndices,
    thicknesses,
):
    """Return reflection for the next layer
    Senkrecht  polarisation"""
    return nextLayerReflection(
        freeSpaceWaveNumber,
        incidentAngle,
        coverRefractiveIndex,
        substrateRefractiveIndices,
        thicknesses,
        calculateSenkrechtTransmission,
        calculateSenkrechtReflection,
    )


def nextLayerReflection(
    freeSpaceWaveNumber,
    incidentAngle,
    coverRefractiveIndex,
    substrateRefractiveIndices,
    thicknesses,
    calculateTransmission,
    calculateReflection,
):
    """Return reflection for the next layer
    Parallel  polarisation"""

    # Base quantities
    filmRefractiveIndex = substrateRefractiveIndices.pop()
    transmissionAngle = calculateTransmissionAngle(
        coverRefractiveIndex, filmRefractiveIndex, incidentAngle
    )
    reflectionInto = calculateReflection(
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
            calculateTransmission,
            calculateReflection,
        )

        transmissionInto = calculateTransmission(
            coverRefractiveIndex, filmRefractiveIndex, incidentAngle, transmissionAngle
        )
        transmissionBack = calculateTransmission(
            filmRefractiveIndex, coverRefractiveIndex, transmissionAngle, incidentAngle
        )

        phaseDifference = calculatePhaseDifference(
            freeSpaceWaveNumber, filmRefractiveIndex, filmThickness, transmissionAngle
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
    freeSpaceWaveVector, filmRefractiveIndex, filmThickness, rayAngle
):
    """The phase difference
    between two parallel rays reflected at thin film interfaces"""
    opticalThickness = filmRefractiveIndex * filmThickness
    opticalPathLength = 2 * opticalThickness * cos(rayAngle)
    return freeSpaceWaveVector * opticalPathLength


def calculateFilmReflection(
    accumulatedPhase,
    reflectionInto,
    reflectionOutOf,
    transmissionInto,
    transmissionBack,
):
    """Fabry Perot reflection coefficient"""
    accumulatedPhase = exp(-1j * accumulatedPhase)
    numerator = transmissionInto * reflectionOutOf * transmissionBack
    demoninator = accumulatedPhase + reflectionInto * reflectionOutOf
    return reflectionInto + numerator / demoninator


def calculateSenkrechtReflection(
    incidentRefractiveIndex,
    transmissionRefractiveIndex,
    incidentAngle,
    transmissionAngle,
):
    """Fresnel reflection coefficient
    Senkrecht polarisation"""
    numerator = incidentRefractiveIndex * cos(
        incidentAngle
    ) - transmissionRefractiveIndex * cos(transmissionAngle)
    denominator = incidentRefractiveIndex * cos(
        incidentAngle
    ) + transmissionRefractiveIndex * cos(transmissionAngle)
    return numerator / denominator


def calculateSenkrechtTransmission(
    incidentRefractiveIndex,
    transmissionRefractiveIndex,
    incidentAngle,
    transmissionAngle,
):
    """Fresnel transmission coefficient
    Senkrecht polarization"""
    numerator = 2 * incidentRefractiveIndex * cos(incidentAngle)
    denominator = incidentRefractiveIndex * cos(
        incidentAngle
    ) + transmissionRefractiveIndex * cos(transmissionAngle)
    return numerator / denominator


def calculateParallelReflection(
    incidentRefractiveIndex,
    transmissionRefractiveIndex,
    incidentAngle,
    transmissionAngle,
):
    """Fresnel reflection coefficient
    Parallel polarisation"""
    numerator = transmissionRefractiveIndex * cos(
        incidentAngle
    ) - incidentRefractiveIndex * cos(transmissionAngle)
    denominator = transmissionRefractiveIndex * cos(
        incidentAngle
    ) + incidentRefractiveIndex * cos(transmissionAngle)
    return numerator / denominator


def calculateParallelTransmission(
    incidentRefractiveIndex,
    transmissionRefractiveIndex,
    incidentAngle,
    transmissionAngle,
):
    """Fresnel transmission coefficient
    Parallel polarisation"""
    numerator = 2 * incidentRefractiveIndex * cos(incidentAngle)
    denominator = transmissionRefractiveIndex * cos(
        incidentAngle
    ) + incidentRefractiveIndex * cos(transmissionAngle)
    return numerator / denominator


def calculateTransmissionAngle(
    incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle
):
    """Calculates the angle of transmission at an interface"""
    sinOfAngleOfTransmission = (
        sin(incidentAngle) * incidenceRefractiveIndex / transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
