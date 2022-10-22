# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import numpy as np
import unittest
from src.fresnel import Parallel, Senkrecht
import src.transmission_angles as ta


class Fresnel(unittest.TestCase):
    def test_Senkrecht_energyconservation(self):

        # Given
        incidentAngle = 15
        coverRefractiveIndex = 1.0
        substrateRefractiveIndex = 1.5
        transmissionAngle = ta.calculate_transmission_angle(
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
        transmissionAngle = ta.calculate_transmission_angle(
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
