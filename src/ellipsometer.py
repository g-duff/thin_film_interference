'''Calculate ellipsometry parameters psi, delta'''

import numpy as np
import functools
from src.transmission_angles import propagate_transmission_angles
from src.fresnel import Parallel, Senkrecht
from src.optical_path import OpticalPath
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
    '''Calculate ellipsometry parameters psi, delta from film stack parameters'''

    refractiveIndexPairs = pairParameters(
        coverRefractiveIndex, filmRefractiveIndexes, substrateRefractiveIndex
    )
    transmittedAngles = propagate_transmission_angles(incidentAngle, refractiveIndexPairs)

    freeSpaceWavenumbers = tau / freeSpaceWavelengths
    pathParameters = zip(filmRefractiveIndexes, filmThicknesses, transmittedAngles)
    accumulatedPhases = [
        OpticalPath(*p).accumulate_phase(freeSpaceWavenumbers) for p in pathParameters
    ]

    anglePairs = pairParameters(
        incidentAngle, transmittedAngles, transmittedAngles.pop()
    )
    opticalInterfaces = [OpticalBoundary(*p) for p in anglePairs]

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
    '''Group list of parameters into pairs'''
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
    '''Reflection from multiple stacked thin films'''
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
    '''Reflection from single thin film'''
    numerator = transmissionInto * reflectionOutOf * transmissionBack
    demoninator = np.exp(-1j * accumulatedPhase) + reflectionInto * reflectionOutOf
    return reflectionInto + numerator / demoninator


def reflectionToPsiDelta(senkrechtReflection, parallelReflection):
    '''Convert reflection coefficients to ellipsometry parameters'''
    reflectionRatio = parallelReflection / senkrechtReflection
    psi = np.arctan(np.abs(reflectionRatio))
    delta = np.angle(reflectionRatio)
    return psi, delta
