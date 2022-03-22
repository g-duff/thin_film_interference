from Fresnel import Parallel, Senkrecht
import ellipsometerUtils as el
import numpy as np
import unittest


class Fresnel(unittest.TestCase):
    def test_fresnelSenkrecht_energyconservation(self):

        # Given
        incidentAngle = 15
        coverRefractiveIndex = 1.0
        substrateRefractiveIndex = 1.5
        transmissionAngle = el.calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefractiveIndex, incidentAngle
        )

        # When
        reflection = Senkrecht.reflection(
            coverRefractiveIndex,
            substrateRefractiveIndex,
            incidentAngle,
            transmissionAngle,
        )
        transmission = Senkrecht.transmission(
            coverRefractiveIndex,
            substrateRefractiveIndex,
            incidentAngle,
            transmissionAngle,
        )

        # Then
        reflectivity = reflection**2
        transmissivity = (
            transmission**2
            * substrateRefractiveIndex
            * np.cos(transmissionAngle)
            / coverRefractiveIndex
            / np.cos(incidentAngle)
        )
        energy = reflectivity + transmissivity
        self.assertAlmostEqual(energy, 1)

    def test_fresnelParallel_energyconservation(self):

        # Given
        incidentAngle = 15
        coverRefractiveIndex = 1.0
        substrateRefrativeIndex = 1.5
        transmissionAngle = el.calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefrativeIndex, incidentAngle
        )

        # When
        reflection = Parallel.reflection(
            coverRefractiveIndex,
            substrateRefrativeIndex,
            incidentAngle,
            transmissionAngle,
        )
        transmission = Parallel.transmission(
            coverRefractiveIndex,
            substrateRefrativeIndex,
            incidentAngle,
            transmissionAngle,
        )

        # Then
        reflectivity = reflection**2
        transmissivity = (
            transmission**2
            * substrateRefrativeIndex
            * np.cos(transmissionAngle)
            / coverRefractiveIndex
            / np.cos(incidentAngle)
        )
        test_energy = reflectivity + transmissivity
        self.assertAlmostEqual(test_energy, 1)
