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
        transmittedAngles = propagateTransmissionAngles(
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

        senkrechtCalculator = FresnelCalculator(Senkrecht)
        senkrechtCoefficients = senkrechtCalculator.prepareCoefficients(
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

        parallelCalculator = FresnelCalculator(Parallel)
        parallelCoefficients = parallelCalculator.prepareCoefficients(
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


class FresnelCalculator:
    def __init__(self, Polarization):
        self.Polarization = Polarization

    def prepareCoefficients(
        self,
        incidentAngle,
        coverRefractiveIndex,
        layers,
    ):
        upperLayers = [(coverRefractiveIndex, incidentAngle)] + layers[:-1]
        layerPairs = zip(upperLayers, layers)
        layerFresnelParameters = []
        for (coverRefractiveIndex, incidentAngle), (
            toRefractiveIndex,
            transmissionAngle,
        ) in layerPairs:
            reflectionInto = self.Polarization.reflection(
                coverRefractiveIndex,
                toRefractiveIndex,
                incidentAngle,
                transmissionAngle,
            )
            transmissionInto = self.Polarization.transmission(
                coverRefractiveIndex,
                toRefractiveIndex,
                incidentAngle,
                transmissionAngle,
            )
            transmissionBack = self.Polarization.transmission(
                toRefractiveIndex,
                coverRefractiveIndex,
                transmissionAngle,
                incidentAngle,
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


def propagateTransmissionAngles(incidentAngle, coverRefractiveIndex, refractiveIndices):
    refractiveIndexPairs = zip(
        [coverRefractiveIndex] + refractiveIndices, refractiveIndices
    )
    return [
        incidentAngle := calculateTransmissionAngle(
            coverRefractiveIndex, refractiveIndex, incidentAngle
        )
        for coverRefractiveIndex, refractiveIndex in refractiveIndexPairs
    ]


def calculateTransmissionAngle(
    incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle
):
    sinOfAngleOfTransmission = (
        sin(incidentAngle) * incidenceRefractiveIndex / transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission
