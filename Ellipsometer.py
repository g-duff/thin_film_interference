import numpy as np
from numpy import cos, sin, exp
from Fresnel import Parallel, Senkrecht
import functools

degrees = np.pi / 180


class Ellipsometer:
    def __init__(self, freeSpaceWavelength):
        self.freeSpaceWavelength = freeSpaceWavelength
        self.freeSpaceWavenumber = 2 * np.pi / freeSpaceWavelength

    def ellipsometry(self, incidentAngle, refractiveIndices, thicknesses):

        coverRefractiveIndex = refractiveIndices.pop(0)
        transmittedAngles = cascadeTransmissionAngle(
            incidentAngle, coverRefractiveIndex, refractiveIndices
        )

        substrateRefractiveIndex = refractiveIndices.pop()
        substrateRayAngle = transmittedAngles.pop()

        phaseDifferences = [
            self.calculatePhaseDifference(transmissionAngle, refractiveIndex, thickness)
            for transmissionAngle, refractiveIndex, thickness in zip(
                transmittedAngles, refractiveIndices, thicknesses
            )
        ]

        layers = list(zip(refractiveIndices, transmittedAngles))

        senkrechtCoefficients = prepareFresnelBusiness(
            Senkrecht,
            incidentAngle,
            coverRefractiveIndex,
            layers,
        )
        senkrechtSubstrateReflection = Senkrecht.reflection(
            refractiveIndices[-1],
            substrateRefractiveIndex,
            transmittedAngles[-1],
            substrateRayAngle,
        )
        senkrechtReflection = combineReflections(
            senkrechtSubstrateReflection,
            phaseDifferences,
            senkrechtCoefficients,
        )
        parallelCoefficients = prepareFresnelBusiness(
            Parallel,
            incidentAngle,
            coverRefractiveIndex,
            layers,
        )
        parallelSubstrateReflection = Parallel.reflection(
            refractiveIndices[-1],
            substrateRefractiveIndex,
            transmittedAngles[-1],
            substrateRayAngle,
        )
        parallelReflection = combineReflections(
            parallelSubstrateReflection,
            phaseDifferences,
            parallelCoefficients,
        )

        return reflectionToPsiDelta(senkrechtReflection, parallelReflection)

    def calculatePhaseDifference(self, rayAngle, filmRefractiveIndex, filmThickness):
        opticalThickness = filmRefractiveIndex * filmThickness
        opticalPathLength = 2 * opticalThickness * cos(rayAngle)
        return self.freeSpaceWavenumber * opticalPathLength


def combineReflections(
    reflectionFromSubstrate,
    phaseDifferences,
    layerFresnelParameters,
):
    return functools.reduce(
        lambda reflectionOutOf, paramSet: calculateFilmReflection(
            reflectionOutOf, *paramSet[0], paramSet[1]
        ),
        zip(layerFresnelParameters[::-1], phaseDifferences[::-1]),
        reflectionFromSubstrate,
    )


def prepareFresnelBusiness(
    Polarization,
    incidentAngle,
    coverRefractiveIndex,
    layers,
):
    layerFresnelParameters = []
    for toRefractiveIndex, transmissionAngle in layers:
        reflectionInto = Polarization.reflection(
            coverRefractiveIndex,
            toRefractiveIndex,
            incidentAngle,
            transmissionAngle,
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

        incidentAngle = transmissionAngle
        coverRefractiveIndex = toRefractiveIndex
        layerFresnelParameters.append(
            [reflectionInto, transmissionInto, transmissionBack]
        )

    return layerFresnelParameters


def reflectionToPsiDelta(senkrechtReflection, parallelReflection):
    reflectionRatio = parallelReflection / senkrechtReflection
    psi = np.arctan(np.abs(reflectionRatio))
    delta = np.angle(reflectionRatio)
    return psi, delta


def calculateFilmReflection(
    reflectionOutOf,
    reflectionInto,
    transmissionInto,
    transmissionBack,
    accumulatedPhase,
):
    numerator = transmissionInto * reflectionOutOf * transmissionBack
    demoninator = exp(-1j * accumulatedPhase) + reflectionInto * reflectionOutOf
    return reflectionInto + numerator / demoninator


def cascadeTransmissionAngle(incidentAngle, coverRefractiveIndex, refractiveIndices):
    rayAngles = []
    for refractiveIndex in refractiveIndices:
        incidentAngle = calculateTransmissionAngle(
            coverRefractiveIndex, refractiveIndex, incidentAngle
        )
        rayAngles.append(incidentAngle)
        coverRefractiveIndex = refractiveIndex

    return rayAngles


def calculateTransmissionAngle(
    incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle
):
    sinOfAngleOfTransmission = (
        sin(incidentAngle) * incidenceRefractiveIndex / transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
