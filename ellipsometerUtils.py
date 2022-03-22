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
        substrateRefractiveIndex = refractiveIndices.pop()

        refractiveIndexPairs = list(
            zip(
                [coverRefractiveIndex] + refractiveIndices,
                refractiveIndices + [substrateRefractiveIndex],
            )
        )
        transmittedAngles = propagateTransmissionAngles(
            incidentAngle, refractiveIndexPairs
        )
        substrateTransmittedAngle = transmittedAngles.pop()

        phaseParameters = zip(transmittedAngles, refractiveIndices, thicknesses)
        phaseDifferences = [
            self.calculatePhaseDifference(transmissionAngle, refractiveIndex, thickness)
            for transmissionAngle, refractiveIndex, thickness in phaseParameters
        ]

        rayAnglePairs = list(
            zip(
                [incidentAngle] + transmittedAngles,
                transmittedAngles + [substrateTransmittedAngle],
            )
        )
        fresnelCalculator = FresnelCalculator(refractiveIndexPairs, rayAnglePairs)

        fresnelCalculator.setPolarization(Senkrecht)
        senkrechtReflection = combineReflections(
            fresnelCalculator,
            phaseDifferences,
        )

        fresnelCalculator.setPolarization(Parallel)
        parallelReflection = combineReflections(
            fresnelCalculator,
            phaseDifferences,
        )

        return reflectionToPsiDelta(senkrechtReflection, parallelReflection)

    def calculatePhaseDifference(self, rayAngle, filmRefractiveIndex, filmThickness):
        opticalThickness = filmRefractiveIndex * filmThickness
        opticalPathLength = 2 * opticalThickness * cos(rayAngle)
        return self.freeSpaceWavenumber * opticalPathLength


class FresnelCalculator:
    def __init__(self, refractiveIndexPairs, rayAnglePairs):
        self.refractiveIndexPairs = refractiveIndexPairs
        self.rayAnglePairs = rayAnglePairs

    def setPolarization(self, Polarization):
        self.Polarization = Polarization

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


def combineReflections(
    fresnelCalculator,
    phaseDifferences,
):

    reflectionInto = fresnelCalculator.reflectionInto()
    transmissionInto = fresnelCalculator.transmissionInto()
    transmissionBack = fresnelCalculator.transmissionBack()
    reflectionFromSubstrate = reflectionInto.pop()
    transmissionInto.pop()
    transmissionBack.pop()
    return functools.reduce(
        lambda reflectionOutOf, paramSet: calculateFilmReflection(
            reflectionOutOf, *paramSet
        ),
        zip(
            reflectionInto[::-1],
            transmissionInto[::-1],
            transmissionBack[::-1],
            phaseDifferences[::-1],
        ),
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
