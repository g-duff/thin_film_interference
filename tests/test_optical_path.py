# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
from src.optical_path import OpticalPath
import unittest
import numpy as np

degrees = np.pi / 180


class accumulatePhase(unittest.TestCase):
    def test_accumulatePhase_normalIncidence(self):
        """Phase difference from reflections indide a film at normal incidence
        tested against film thicknesses of fractional wavelengths"""

        # Given
        tau = 2 * np.pi

        freeSpaceWavelength = 800
        transmissionAngle = 0
        filmRefractiveIndex = 2.0
        freeSpaceWavenumber = tau / freeSpaceWavelength

        comparisonFactors = (0, 1 / 2, 1 / 4, 1 / 6)
        filmThicknesses = [cf * freeSpaceWavelength for cf in comparisonFactors]
        testOpticalPaths = [
            OpticalPath(filmRefractiveIndex, t, transmissionAngle)
            for t in filmThicknesses
        ]

        # When
        actualPhaseDifference = [
            o.accumulate_phase(freeSpaceWavenumber) for o in testOpticalPaths
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

    def test_accumulatePhase_angledincidence(self):
        """Phase difference from reflections indide a film at 60 degrees
        tested against film thicknesses of fractional wavelengths and
        exact cosine values"""

        # Given
        tau = 2 * np.pi
        freeSpaceWavelength = 800
        transmissionAngle = 60 * degrees
        filmRefractiveIndex = 2.0
        freeSpaceWavenumber = tau / freeSpaceWavelength

        comparisonFactors = (0, 1 / 2, 1 / 4, 1 / 6)
        filmThicknesses = [cf * freeSpaceWavelength for cf in comparisonFactors]
        testOpticalPaths = [
            OpticalPath(filmRefractiveIndex, t, transmissionAngle)
            for t in filmThicknesses
        ]

        # When
        actualPhaseDifference = [
            o.accumulate_phase(freeSpaceWavenumber) for o in testOpticalPaths
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


if __name__ == "__main__":
    unittest.main()
