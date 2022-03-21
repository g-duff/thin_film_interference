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
        substrateRefractiveIndex = refractiveIndices.pop()
        layers = list(zip(refractiveIndices, thicknesses))

        senkrechtReflection = self.iterativeLayerReflection(
            Senkrecht,
            incidentAngle,
            coverRefractiveIndex,
            substrateRefractiveIndex,
            layers,
        )
        parallelReflection = self.iterativeLayerReflection(
            Parallel,
            incidentAngle,
            coverRefractiveIndex,
            substrateRefractiveIndex,
            layers,
        )

        return reflectionToPsiDelta(senkrechtReflection, parallelReflection)

    def iterativeLayerReflection(
        self,
        Polarization,
        incidentAngle,
        coverRefractiveIndex,
        substrateRefractiveIndex,
        layers,
    ):
        layerFresnelParameters = []
        for toRefractiveIndex, thickness in layers:
            transmissionAngle = calculateTransmissionAngle(
                coverRefractiveIndex, toRefractiveIndex, incidentAngle
            )
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
            phaseDifference = self.calculatePhaseDifference(
                transmissionAngle, toRefractiveIndex, thickness
            )
            incidentAngle = transmissionAngle
            coverRefractiveIndex = toRefractiveIndex
            layerFresnelParameters.append(
                [reflectionInto, transmissionInto, transmissionBack, phaseDifference]
            )

        transmissionAngle = calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefractiveIndex, incidentAngle
        )
        reflectionFromSubstrate = Polarization.reflection(
            coverRefractiveIndex,
            substrateRefractiveIndex,
            incidentAngle,
            transmissionAngle,
        )

        return functools.reduce(
            lambda reflectionOutOf, paramSet: calculateFilmReflection(
                reflectionOutOf, *paramSet
            ),
            layerFresnelParameters[::-1],
            reflectionFromSubstrate,
        )

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
    reflectionOutOf,
    reflectionInto,
    transmissionInto,
    transmissionBack,
    accumulatedPhase,
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
