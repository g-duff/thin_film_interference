import numpy as np
import functools
from src.transmissionAngleService import propagateTransmissionAngles
from src.fresnel import Parallel, Senkrecht
from src.opticalPathDomain import OpticalPath
from src.optical_boundary import OpticalBoundary

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

    freeSpaceWavenumbers = tau / freeSpaceWavelengths
    pathParameters = zip(filmRefractiveIndexes, filmThicknesses, transmittedAngles)
    accumulatedPhases = [
        OpticalPath(*p).accumulatePhase(freeSpaceWavenumbers) for p in pathParameters
    ]

    anglePairs = pairParameters(
        incidentAngle, transmittedAngles, transmittedAngles.pop()
    )
    interfaceParameters = zip(refractiveIndexPairs, anglePairs)
    opticalInterfaces = [OpticalBoundary(*p) for p in interfaceParameters]

    substrateInterface = opticalInterfaces.pop()

    for o in opticalInterfaces + [substrateInterface]:
        o.set_polarization(Parallel)

    parallelReflection = filmStackResponse(
        opticalInterfaces, accumulatedPhases, substrateInterface
    )

    for o in opticalInterfaces + [substrateInterface]:
        o.set_polarization(Senkrecht)

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


def filmStackResponse(
    opticalInterfaces,
    accumulatedPhases,
    substrateInterface,
):
    return functools.reduce(
        lambda reflectionOutOf, opticalProperties: calculateFilmReflection(
            reflectionOutOf,
            opticalProperties[0].reflection_into(),
            opticalProperties[0].transmission_into(),
            opticalProperties[0].transmission_back(),
            opticalProperties[1],
        ),
        zip(opticalInterfaces[::-1], accumulatedPhases[::-1]),
        substrateInterface.reflection_into(),
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
