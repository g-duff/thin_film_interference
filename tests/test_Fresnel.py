from src.fresnel import Parallel, Senkrecht
import src.transmission_angles as ta
import numpy as np
import unittest


class Fresnel(unittest.TestCase):
    def test_Senkrecht_energyconservation(self):

        # Given
        incidentAngle = 15
        coverRefractiveIndex = 1.0
        substrateRefractiveIndex = 1.5
        transmissionAngle = ta.calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefractiveIndex, incidentAngle
        )

        # When
        reflection = Senkrecht.reflection(
            incidentAngle,
            transmissionAngle,
        )
        transmission = Senkrecht.transmission(
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

    def test_Parallel_energyconservation(self):

        # Given
        incidentAngle = 15
        coverRefractiveIndex = 1.0
        substrateRefrativeIndex = 1.5
        transmissionAngle = ta.calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefrativeIndex, incidentAngle
        )

        # When
        reflection = Parallel.reflection(
            incidentAngle,
            transmissionAngle,
        )
        transmission = Parallel.transmission(
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
