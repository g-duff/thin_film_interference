# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
import thin_film_interference.ellipsometer as ec


class Ellipsometry(unittest.TestCase):
    def test_against_regres_pro(self):
        # Given
        free_space_wavelength, expected_tan_psi, expected_cos_delta = np.genfromtxt(
            "./test/SoI_regressPro.txt", skip_header=1, unpack=True, usecols=(0, 2, 5)
        )

        substrate_refractive_index = 3.8
        cover_refractive_index = 1.0
        refractive_indices = [cover_refractive_index] + [3.8, 1.45] + [substrate_refractive_index]
        film_thicknesses = [220, 3000]
        incident_angle = np.deg2rad(65)

        # When
        psi, delta = ec.ellipsometry(
            free_space_wavelength,
            incident_angle,
            refractive_indices,
            film_thicknesses,
        )

        # Then
        tan_psi_residuals = np.tan(psi) - expected_tan_psi
        cos_delta_residuals = np.cos(delta) - expected_cos_delta

        tan_psi_residuals = sum(tan_psi_residuals)
        cos_delta_residuals = sum(cos_delta_residuals)
        total_residuals = round(tan_psi_residuals + cos_delta_residuals, 4)

        self.assertAlmostEqual(total_residuals, 0)
