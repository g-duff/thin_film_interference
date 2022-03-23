import numpy as np
import functools
from src.fresnel import Parallel, Senkrecht
from src.opticalPathDomain import OpticalPath
from src.opticalInterfaceDomain import OpticalInterface

tau = 2 * np.pi

def ellipsometry(
    freeSpaceWavelengths,
    incidentAngle,
    filmRefractiveIndexes,
    filmThicknesses,
    substrateRefractiveIndex,
    coverRefractiveIndex=1,
):

    refractiveIndexPairs = pairParameters(
        coverRefractiveIndex, filmRefractiveIndexes, substrateRefractiveIndex
    )
    transmittedAngles = propagateTransmissionAngles(incidentAngle, refractiveIndexPairs)

    pathParameters = zip(filmRefractiveIndexes, filmThicknesses, transmittedAngles)
    opticalPaths = (OpticalPath(*p) for p in pathParameters)
    freeSpaceWavenumbers = tau / freeSpaceWavelengths
    accumulatedPhases = [p.accumulatePhase(freeSpaceWavenumbers) for p in opticalPaths]

    anglePairs = pairParameters(
        incidentAngle, transmittedAngles, transmittedAngles.pop()
    )

    interfaceParameters = zip(refractiveIndexPairs, anglePairs)
    opticalInterfaces = [OpticalInterface(*p) for p in interfaceParameters]
    substrateInterface = opticalInterfaces.pop()

    for o in opticalInterfaces:
        o.setPolarization(Parallel)
    substrateInterface.setPolarization(Parallel)

    parallelReflection = filmStackResponse(
        opticalInterfaces, accumulatedPhases, substrateInterface
    )

    for o in opticalInterfaces:
        o.setPolarization(Senkrecht)
    substrateInterface.setPolarization(Senkrecht)

    senkrechtReflection = filmStackResponse(
        opticalInterfaces, accumulatedPhases, substrateInterface
    )

    return reflectionToPsiDelta(senkrechtReflection, parallelReflection)


def pairParameters(firstItem, middleItems, lastItem):
    return list(
        zip(
            [firstItem] + middleItems,
            middleItems + [lastItem],
        )
    )


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
        np.sin(incidentAngle) * incidenceRefractiveIndex / transmissionRefractiveIndex
    )
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission


def filmStackResponse(
    opticalInterfaces,
    accumulatedPhases,
    substrateInterface,
):
    return functools.reduce(
        lambda reflectionOutOf, opticalProperties: calculateFilmReflection(
            reflectionOutOf,
            opticalProperties[0].reflectionInto(),
            opticalProperties[0].transmissionInto(),
            opticalProperties[0].transmissionBack(),
            opticalProperties[1],
        ),
        zip(opticalInterfaces[::-1], accumulatedPhases[::-1]),
        substrateInterface.reflectionInto(),
    )


def calculateFilmReflection(
    reflectionOutOf,
    reflectionInto,
    transmissionInto,
    transmissionBack,
    accumulatedPhase,
):
    numerator = transmissionInto * reflectionOutOf * transmissionBack
    demoninator = np.exp(-1j * accumulatedPhase) + reflectionInto * reflectionOutOf
    return reflectionInto + numerator / demoninator


def reflectionToPsiDelta(senkrechtReflection, parallelReflection):
    reflectionRatio = parallelReflection / senkrechtReflection
    psi = np.arctan(np.abs(reflectionRatio))
    delta = np.angle(reflectionRatio)
    return psi, delta
