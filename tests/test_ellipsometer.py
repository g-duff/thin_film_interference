import src.ellipsometer as ec
import unittest
import numpy as np


class Ellipsometry(unittest.TestCase):
    def test_regpro_SoI(self):
        # Given
        freeSpaceWavelength, expectedTanPsi, expectedCosDelta = np.genfromtxt(
            "./tests/SoI_regressPro.txt", skip_header=1, unpack=True, usecols=(0, 2, 5)
        )

        substrateRefractiveIndex = 3.8
        coverRefractiveIndex = 1.0
        refractiveIndices = [3.8, 1.45]
        filmThicknesses = [220, 3000]
        incidentAngle = np.deg2rad(65)

        # When
        psi, delta = ec.ellipsometry(
            freeSpaceWavelength,
            incidentAngle,
            refractiveIndices,
            filmThicknesses,
            substrateRefractiveIndex,
            coverRefractiveIndex,
        )

        # Then
        tanPsiResiduals = np.tan(psi) - expectedTanPsi
        cosDeltaResiduals = np.cos(delta) - expectedCosDelta

        tanPsiResiduals = sum(tanPsiResiduals)
        cosDeltaResiduals = sum(cosDeltaResiduals)
        totalResiduals = round(tanPsiResiduals + cosDeltaResiduals, 4)

        self.assertAlmostEqual(totalResiduals, 0)
