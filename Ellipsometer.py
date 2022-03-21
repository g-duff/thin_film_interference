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

        refractiveIndexPairs = list(
            zip([coverRefractiveIndex] + refractiveIndices, refractiveIndices)
        )
        transmittedAngles = propagateTransmissionAngles(
            incidentAngle, refractiveIndexPairs
        )

        filmRefractiveIndices = refractiveIndices[:-1]
        phaseParameters = zip(transmittedAngles, filmRefractiveIndices, thicknesses)
        phaseDifferences = [
            self.calculatePhaseDifference(transmissionAngle, refractiveIndex, thickness)
            for transmissionAngle, refractiveIndex, thickness in phaseParameters
        ]

        rayAnglePairs = list(
            zip([incidentAngle] + transmittedAngles, transmittedAngles)
        )
        senkrechtCalculator = FresnelCalculator(
            Senkrecht, refractiveIndexPairs, rayAnglePairs
        )
        senkrechtCoefficients = senkrechtCalculator.prepareCoefficients()
        senkrechtSubstrateReflection = senkrechtCoefficients.pop()
        senkrechtReflection = combineReflections(
            senkrechtSubstrateReflection[0],
            phaseDifferences,
            senkrechtCoefficients,
        )

        parallelCalculator = FresnelCalculator(
            Parallel, refractiveIndexPairs, rayAnglePairs
        )
        parallelCoefficients = parallelCalculator.prepareCoefficients()
        parallelSubstrateReflection = parallelCoefficients.pop()
        parallelReflection = combineReflections(
            parallelSubstrateReflection[0],
            phaseDifferences,
            parallelCoefficients,
        )

        return reflectionToPsiDelta(senkrechtReflection, parallelReflection)

    def calculatePhaseDifference(self, rayAngle, filmRefractiveIndex, filmThickness):
        opticalThickness = filmRefractiveIndex * filmThickness
        opticalPathLength = 2 * opticalThickness * cos(rayAngle)
        return self.freeSpaceWavenumber * opticalPathLength


class FresnelCalculator:
    def __init__(self, Polarization, refractiveIndexPairs, rayAnglePairs):
        self.Polarization = Polarization
        self.refractiveIndexPairs = refractiveIndexPairs
        self.rayAnglePairs = rayAnglePairs

    def reflectionInto(self):
        return [
            self.Polarization.reflection(
                *refractiveIndices,
                *rayAngles,
            )
            for refractiveIndices, rayAngles in zip(
                self.refractiveIndexPairs, self.rayAnglePairs
            )
        ]

    def transmissionInto(self):
        return [
            self.Polarization.transmission(
                *refractiveIndices,
                *rayAngles,
            )
            for refractiveIndices, rayAngles in zip(
                self.refractiveIndexPairs, self.rayAnglePairs
            )
        ]

    def transmissionBack(self):
        return [
            self.Polarization.transmission(
                *refractiveIndices[::-1],
                *rayAngles[::-1],
            )
            for refractiveIndices, rayAngles in zip(
                self.refractiveIndexPairs, self.rayAnglePairs
            )
        ]

    def prepareCoefficients(self):
        return list(zip(self.reflectionInto(), self.transmissionInto(), self.transmissionBack()))


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
