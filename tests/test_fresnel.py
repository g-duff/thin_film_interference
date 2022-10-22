# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
from src.fresnel import Parallel, Senkrecht
import src.transmission_angles as ta
import numpy as np
import unittest


class Fresnel(unittest.TestCase):
    def test_senkrecht_energyconservation(self):

        # Given
        incident_angle = 15
        cover_refractive_index = 1.0
        substrate_refractive_index = 1.5
        transmission_angle = ta.calculate_transmission_angle(
            cover_refractive_index, substrate_refractive_index, incident_angle
        )

        # When
        reflection = Senkrecht.reflection(
            incident_angle,
            transmission_angle,
        )
        transmission = Senkrecht.transmission(
            incident_angle,
            transmission_angle,
        )

        # Then
        reflectivity = reflection**2
        transmissivity = (
            transmission**2
            * substrate_refractive_index
            * np.cos(transmission_angle)
            / cover_refractive_index
            / np.cos(incident_angle)
        )
        energy = reflectivity + transmissivity
        self.assertAlmostEqual(energy, 1)

    def test_parallel_energyconservation(self):

        # Given
        incident_angle = 15
        cover_refractive_index = 1.0
        substrate_refrative_index = 1.5
        transmission_angle = ta.calculate_transmission_angle(
            cover_refractive_index, substrate_refrative_index, incident_angle
        )

        # When
        reflection = Parallel.reflection(
            incident_angle,
            transmission_angle,
        )
        transmission = Parallel.transmission(
            incident_angle,
            transmission_angle,
        )

        # Then
        reflectivity = reflection**2
        transmissivity = (
            transmission**2
            * substrate_refrative_index
            * np.cos(transmission_angle)
            / cover_refractive_index
            / np.cos(incident_angle)
        )
        test_energy = reflectivity + transmissivity
        self.assertAlmostEqual(test_energy, 1)
