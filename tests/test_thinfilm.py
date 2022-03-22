import ellipsometerUtils as el
import unittest
import numpy as np


class BaseFunctions(unittest.TestCase):
    def test_calculateAngleOfTransmission_normalIncidence(self):
        """Snell's law at normal incidence"""
        # Given
        coverRefractiveIndex = 1.0
        substrateRefractiveIndex = 1.5
        incidentAngle = 0

        # When
        transmissionAngle = el.calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefractiveIndex, incidentAngle
        )

        # Then
        self.assertEqual(transmissionAngle, 0)

    def test_calculateAngleOfTransmission_obliqueIncidence(self):
        """Snell's law, incident at 45 degrees tested
        against exact sine values for total internal reflection"""
        # Given
        coverRefractiveIndex = 2
        substrateRefractiveIndex = np.sqrt(2)
        incidentAngle = 45 * el.degrees

        # When
        transmissionAngle = el.calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefractiveIndex, incidentAngle
        )

        # Then
        self.assertAlmostEqual(transmissionAngle, np.pi / 2)

    def test_calculatePhaseDifference_normalIncidence(self):
        """Phase difference from reflections indide a film at normal incidence
        tested against film thicknesses of fractional wavelengths"""

        # Given
        tau = 2 * np.pi

        freeSpaceWavelength = 800
        transmissionAngle = 0
        filmRefractiveIndex = 2.0

        comparisonFactors = (0, 1 / 2, 1 / 4, 1 / 6)

        filmThicknesses = [cf * freeSpaceWavelength for cf in comparisonFactors]
        testEllipsometer = el.Ellipsometer(freeSpaceWavelength)

        # When
        actualPhaseDifference = [
            testEllipsometer.calculatePhaseDifference(
                transmissionAngle, filmRefractiveIndex, t
            )
            for t in filmThicknesses
        ]

        # Then
        expectedPhaseDifference = [
            cf * 2 * filmRefractiveIndex * tau for cf in comparisonFactors
        ]
        phaseResiduals = (
            pout - pcomp
            for pout, pcomp in zip(actualPhaseDifference, expectedPhaseDifference)
        )
        phaseResiduals = sum(phaseResiduals)

        self.assertAlmostEqual(phaseResiduals, 0)

    def test_calculatePhaseDifference_angledincidence(self):
        """Phase difference from reflections indide a film at 60 degrees
        tested against film thicknesses of fractional wavelengths and
        exact cosine values"""

        # Given
        tau = 2 * np.pi
        freeSpaceWavelength = 800
        transmissionAngle = 60 * el.degrees
        filmRefractiveIndex = 2.0

        comparisonFactors = (0, 1 / 2, 1 / 4, 1 / 6)
        filmThicknesses = [cf * freeSpaceWavelength for cf in comparisonFactors]
        testEllipsometer = el.Ellipsometer(freeSpaceWavelength)

        # When
        actualPhaseDifference = [
            testEllipsometer.calculatePhaseDifference(
                transmissionAngle, filmRefractiveIndex, t
            )
            for t in filmThicknesses
        ]

        # Then
        expectedPhaseDifference = [
            cf * 2 * filmRefractiveIndex * tau * 0.5 for cf in comparisonFactors
        ]
        phaseResiduals = (
            pout - pcomp
            for pout, pcomp in zip(actualPhaseDifference, expectedPhaseDifference)
        )
        phaseResiduals = sum(phaseResiduals)

        self.assertAlmostEqual(phaseResiduals, 0)


class Ellipsometry(unittest.TestCase):
    def test_regpro_SoI(self):
        """Compare calculated psi and delta values for SoI thin film against
        output from the Regress Pro application
        using the same input parameters"""

        freeSpaceWavelength, expectedTanPsi, expectedCosDelta = np.genfromtxt(
            "./tests/SoI_regressPro.txt", skip_header=1, unpack=True, usecols=(0, 2, 5)
        )

        # Given
        refractiveIndices = [1.0, 3.8, 1.45, 3.8]
        filmThicknesses = [220, 3000]
        incidentAngle = 65 * el.degrees

        # When
        testEllipsometer = el.Ellipsometer(freeSpaceWavelength)
        psi, delta = testEllipsometer.ellipsometry(
            incidentAngle, refractiveIndices, filmThicknesses
        )

        # Then
        tanPsiResiduals = np.tan(psi) - expectedTanPsi
        cosDeltaResiduals = np.cos(delta) - expectedCosDelta

        tanPsiResiduals = sum(tanPsiResiduals)
        cosDeltaResiduals = sum(cosDeltaResiduals)
        totalResiduals = round(tanPsiResiduals + cosDeltaResiduals, 4)

        self.assertAlmostEqual(totalResiduals, 0)


if __name__ == "__main__":
    unittest.main()
