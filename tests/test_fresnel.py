# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
from src.fresnel import Parallel, Senkrecht
import src.transmission_angles as ta


class Fresnel(unittest.TestCase):
    def test_senkrecht_energyconservation(self):

        # Given
        incident_angle = np.deg2rad(15)
        cover_refractive_index = 1.0
        substrate_refractive_index = 1.5
        transmission_angle = ta.calculate_transmission_angle(
            cover_refractive_index, substrate_refractive_index, incident_angle
        )

        incident_wavevector_normal_component = cover_refractive_index * \
            np.cos(incident_angle)
        transmission_wavevector_normal_component = substrate_refractive_index * \
            np.cos(transmission_angle)

        # When
        reflection = Senkrecht.reflection(
            incident_wavevector_normal_component,
            transmission_wavevector_normal_component,
        )
        transmission = Senkrecht.transmission(
            incident_wavevector_normal_component,
            transmission_wavevector_normal_component,
        )

        # Then
        self.assertAlmostEqual(transmission, reflection + 1)

    def test_parallel_energyconservation(self):

        # Given
        incident_angle = np.deg2rad(15)
        cover_refractive_index = 1.0
        substrate_refractive_index = 1.5
        transmission_angle = ta.calculate_transmission_angle(
            cover_refractive_index, substrate_refractive_index, incident_angle
        )

        incident_wavevector_normal_component = cover_refractive_index * \
            np.cos(incident_angle)
        transmission_wavevector_normal_component = substrate_refractive_index * \
            np.cos(transmission_angle)

        # When
        reflection = Parallel.reflection(
            incident_wavevector_normal_component,
            transmission_wavevector_normal_component,
            cover_refractive_index,
            substrate_refractive_index,
        )
        transmission = Parallel.transmission(
            incident_wavevector_normal_component,
            transmission_wavevector_normal_component,
            cover_refractive_index,
            substrate_refractive_index,
        )

        # Then
        self.assertAlmostEqual(
            transmission * substrate_refractive_index/cover_refractive_index, reflection + 1)
