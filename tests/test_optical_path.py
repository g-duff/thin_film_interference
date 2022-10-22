# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
from src.optical_path import accumulate_phase

degrees = np.pi / 180


class AccumulatePhase(unittest.TestCase):
    def test_accumulate_phase_normal_incidence(self):
        """Phase difference from reflections indide a film at normal incidence
        tested against film thicknesses of fractional wavelengths"""

        # Given
        tau = 2 * np.pi

        free_space_wavelength = 800
        transmission_angle = 0
        wavenumber = tau / free_space_wavelength

        comparison_factors = (0, 1 / 2, 1 / 4, 1 / 6)
        film_thicknesses = [
            cf * free_space_wavelength for cf in comparison_factors]

        # When
        actual_phase_difference = [
            accumulate_phase(wavenumber, transmission_angle, t)
            for t in film_thicknesses
        ]

        # Then
        expected_phase_difference = [
            cf * tau * 2 for cf in comparison_factors
        ]
        phase_residuals = (
            pout - pcomp
            for pout, pcomp in zip(actual_phase_difference, expected_phase_difference)
        )
        phase_residuals = sum(phase_residuals)

        self.assertAlmostEqual(phase_residuals, 0)

    def test_accumulate_phase_angledincidence(self):
        """Phase difference from reflections indide a film at 60 degrees
        tested against film thicknesses of fractional wavelengths and
        exact cosine values"""

        # Given
        tau = 2 * np.pi
        free_space_wavelength = 800
        transmission_angle = 60 * degrees
        wavenumber = tau / free_space_wavelength

        comparison_factors = (0, 1 / 2, 1 / 4, 1 / 6)
        film_thicknesses = [
            cf * free_space_wavelength for cf in comparison_factors]

        # When
        actual_phase_difference = [
            accumulate_phase(wavenumber, transmission_angle, t)
            for t in film_thicknesses
        ]
        # Then
        expected_phase_difference = [
            cf * tau for cf in comparison_factors
        ]
        phase_residuals = (
            pout - pcomp
            for pout, pcomp in zip(actual_phase_difference, expected_phase_difference)
        )
        phase_residuals = sum(phase_residuals)

        self.assertAlmostEqual(phase_residuals, 0)


if __name__ == "__main__":
    unittest.main()
