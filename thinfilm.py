import numpy as np
from numpy import cos, sin, exp
import cmath

'''Library for calculating reflection from a thin film

 |
 |          Layer 1
 |
\ / incident
-------------------------------
            Layer 2
-------------------------------
            Layer 3
-------------------------------

'''

# Constants

degrees = np.pi/180


def calculateAngleOfTransmission(incidenceRefractiveIndex, transmissionRefractiveIndex, incidentAngle):
    '''Calculates the angle of transmission at an interface'''
    sinOfAngleOfTransmission = sin(incidentAngle)*incidenceRefractiveIndex/transmissionRefractiveIndex
    angleOfTransmission = np.arcsin(sinOfAngleOfTransmission)
    return angleOfTransmission


def calculatePhaseDifference(freeSpaceWaveVector, filmRefractiveIndex, filmThickness, rayAngle):
    ''' The phase difference 
    between two parallel rays reflected at thin film interfaces'''
    opticalThickness = filmRefractiveIndex*filmThickness
    opticalPathLength = 2*opticalThickness*cos(rayAngle)
    return freeSpaceWaveVector * opticalPathLength


def calculateSenkrechtReflection(incidentRefractiveIndex, transmissionRefractiveIndex, incidentAngle, transmissionAngle):
    ''' Fresnel reflection coefficient
    Senkrecht polarisation'''
    numerator = (incidentRefractiveIndex*cos(incidentAngle)-transmissionRefractiveIndex*cos(transmissionAngle))
    denominator = (incidentRefractiveIndex*cos(incidentAngle)+transmissionRefractiveIndex*cos(transmissionAngle))
    return numerator/denominator


def calculateSenkrechtTransmission(incidentRefractiveIndex, transmissionRefractiveIndex, incidentAngle, transmissionAngle):
    ''' Fresnel transmission coefficient
    Senkrecht polarization'''
    numerator = 2*incidentRefractiveIndex*cos(incidentAngle)
    denominator = (incidentRefractiveIndex*cos(incidentAngle) + transmissionRefractiveIndex*cos(transmissionAngle))
    return numerator/denominator


def calculateParallelReflection(incidentRefractiveIndex, transmissionRefractiveIndex, incidentAngle, transmissionAngle):
    ''' Fresnel reflection coefficient
    Parallel polarisation'''
    numerator = (transmissionRefractiveIndex*cos(incidentAngle)-incidentRefractiveIndex*cos(transmissionAngle))
    denominator = (transmissionRefractiveIndex*cos(incidentAngle)+incidentRefractiveIndex*cos(transmissionAngle))
    return numerator/denominator


def calculateParallelTransmission(incidentRefractiveIndex, transmissionRefractiveIndex, incidentAngle, transmissionAngle):
    ''' Fresnel transmission coefficient
    Parallel polarisation'''
    numerator = 2*incidentRefractiveIndex*cos(incidentAngle)
    denominator = (transmissionRefractiveIndex*cos(incidentAngle) + incidentRefractiveIndex*cos(transmissionAngle))
    return numerator/denominator


def calculateFilmReflection(accumulatedPhase, reflectionInto, reflectionOutOf, transmissionInto, transmissionBack):
    ''' Fabry Perot reflection coefficient '''
    accumulatedPhase = exp(-1j*accumulatedPhase)
    numerator = transmissionInto*reflectionOutOf*transmissionBack
    demoninator = accumulatedPhase+reflectionInto*reflectionOutOf
    return reflectionInto + numerator/demoninator


def reflectionToPsiDelta(senkrechtReflection, parallelReflection):
    '''Return psi and delta ellipsometry parameters from reflection coefficients'''
    reflectionRatio = parallelReflection/senkrechtReflection
    psi = np.arctan(np.abs(reflectionRatio))
    delta = np.angle(reflectionRatio)
    return psi, delta


def nextLayerSenkrechtReflection(freeSpaceWaveNumber, indidentAngle, coverRefractiveIndex, substrateRefractiveIndices, thicknesses):
    ''' Return reflection for the next layer 
    Senkrecht polarisation'''

    # Base quantities
    filmRefractiveIndex = substrateRefractiveIndices.pop()
    transmissionAngle = calculateAngleOfTransmission(coverRefractiveIndex, filmRefractiveIndex, indidentAngle)
    reflectionInto = calculateSenkrechtReflection(coverRefractiveIndex, filmRefractiveIndex, indidentAngle, transmissionAngle)

    try:
        # Interference inside a thin film, calculated using
        # a Fabry-Perot model
        filmThickness = thicknesses.pop()
        reflectionOutOf = nextLayerSenkrechtReflection(freeSpaceWaveNumber, transmissionAngle, filmRefractiveIndex, substrateRefractiveIndices, thicknesses)

        transmissionInto = calculateSenkrechtTransmission(coverRefractiveIndex, filmRefractiveIndex, indidentAngle, transmissionAngle)
        transmissionBack = calculateSenkrechtTransmission(filmRefractiveIndex, coverRefractiveIndex, transmissionAngle, indidentAngle)

        phaseDifference = calculatePhaseDifference(freeSpaceWaveNumber, filmRefractiveIndex, filmThickness, transmissionAngle)

        reflectionInto = calculateFilmReflection(phaseDifference, reflectionInto, reflectionOutOf, transmissionInto, transmissionBack)

    except IndexError:
        # Reflectance for a single interface when
        # no finite thicknesses are left in the stack
        pass

    finally:
        return reflectionInto


def nextLayerParallelReflection(freeSpaceWaveNumber, incidentAngle, coverRefractiveIndex, substrateRefractiveIndices, thicknesses):
    ''' Return reflection for the next layer 
    Parallel  polarisation'''

    # Base quantities
    filmRefractiveIndex = substrateRefractiveIndices.pop()
    transmissionAngle = calculateAngleOfTransmission(coverRefractiveIndex, filmRefractiveIndex, incidentAngle)
    reflectionInto = calculateParallelReflection(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, transmissionAngle)

    try:
        # Interference inside a thin film, calculated using
        # a Fabry-Perot model
        filmThickness = thicknesses.pop()
        reflectionOutOf = nextLayerParallelReflection(freeSpaceWaveNumber, transmissionAngle, filmRefractiveIndex, substrateRefractiveIndices, thicknesses)

        transmissionInto = calculateParallelTransmission(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, transmissionAngle)
        transmissionBack = calculateParallelTransmission(filmRefractiveIndex, coverRefractiveIndex, transmissionAngle, incidentAngle)

        phaseDifference = calculatePhaseDifference(freeSpaceWaveNumber, filmRefractiveIndex, filmThickness, transmissionAngle)

        reflectionInto = calculateFilmReflection(phaseDifference, reflectionInto, reflectionOutOf, transmissionInto, transmissionBack)

    except IndexError:
        # Reflectance for a single interface when
        # no finite thicknesses are left in the stack
        pass

    finally:
        return reflectionInto


def ellipsometry(lambda_0, theta_i, ref_indices, thicknesses):
    '''Ellipsometry parameters for an n-layer thin film stack'''

    k0 = 2*np.pi/lambda_0

    ref_indices.reverse()
    thicknesses.reverse()

    n_cov = ref_indices.pop()

    r_s = nextLayerSenkrechtReflection(k0, theta_i, n_cov, ref_indices[:], thicknesses[:])
    r_p = nextLayerParallelReflection(k0, theta_i, n_cov, ref_indices[:], thicknesses[:])

    psi, delta = reflectionToPsiDelta(r_s, r_p)

    return psi, delta
