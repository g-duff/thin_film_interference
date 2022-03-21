import numpy as np
from numpy import cos, sin, exp
from Fresnel import Parallel, Senkrecht
import functools

degrees = np.pi / 180
tau = 2 * np.pi


class Ellipsometer:
    def __init__(self, freeSpaceWavelength):
        self.freeSpaceWavelength = freeSpaceWavelength
        self.freeSpaceWavenumber = tau / freeSpaceWavelength

    def ellipsometry(self, incidentAngle, refractiveIndices, thicknesses):

        coverRefractiveIndex = refractiveIndices.pop(0)
        filmRefractiveIndices = refractiveIndices[:-1]

        refractiveIndexPairs = list(
            zip([coverRefractiveIndex] + refractiveIndices, refractiveIndices)
        )
        transmittedAngles = propagateTransmissionAngles(
            incidentAngle, refractiveIndexPairs
        )
        phaseDifferences = [
            self.calculatePhaseDifference(transmissionAngle, refractiveIndex, thickness)
            for transmissionAngle, refractiveIndex, thickness in zip(
                transmittedAngles, filmRefractiveIndices, thicknesses
            )
        ]

        rayAnglePairs = list(
            zip([incidentAngle] + transmittedAngles, transmittedAngles)
        )
        finalAnglePair = rayAnglePairs.pop()
        finalRefractiveIndexPair = refractiveIndexPairs.pop()

        senkrechtCalculator = FresnelCalculator(Senkrecht)
        senkrechtCoefficients = senkrechtCalculator.prepareCoefficients(
            refractiveIndexPairs, rayAnglePairs
        )
        senkrechtSubstrateReflection = Senkrecht.reflection(
            *finalRefractiveIndexPair,
            *finalAnglePair
        )
        senkrechtReflection = combineReflections(
            senkrechtSubstrateReflection,
            phaseDifferences,
            senkrechtCoefficients,
        )

        parallelCalculator = FresnelCalculator(Parallel)
        parallelCoefficients = parallelCalculator.prepareCoefficients(
            refractiveIndexPairs, rayAnglePairs
        )
        parallelSubstrateReflection = Parallel.reflection(
            *finalRefractiveIndexPair,
            *finalAnglePair
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


class FresnelCalculator:
    def __init__(self, Polarization):
        self.Polarization = Polarization

    def prepareCoefficients(self, refractiveIndexPairs, rayAnglePairs):
        layerFresnelParameters = []
        for refractiveIndices, rayAngles in zip(refractiveIndexPairs, rayAnglePairs):
            reflectionInto = self.Polarization.reflection(
                *refractiveIndices,
                *rayAngles,
            )
            transmissionInto = self.Polarization.transmission(
                *refractiveIndices,
                *rayAngles,
            )
            transmissionBack = self.Polarization.transmission(
                *refractiveIndices[::-1],
                *rayAngles[::-1],
            )
            layerFresnelParameters.append(
                [reflectionInto, transmissionInto, transmissionBack]
            )

        return layerFresnelParameters


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


def propagateTransmissionAngles(incidentAngle, refractiveIndexPairs):
    return [
        incidentAngle := calculateTransmissionAngle(
            coverRefractiveIndex, lowerRefractiveIndex, incidentAngle
        )
        for coverRefractiveIndex, lowerRefractiveIndex in refractiveIndexPairs
    ]


def calculateTransmissionAngle(
    incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle
):
    sinOfAngleOfTransmission = (
        sin(incidentAngle) * incidenceRefractiveIndex / transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
