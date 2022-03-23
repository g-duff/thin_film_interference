import src.ellipsometerService as el
import unittest
import numpy as np


class transmissionAngles(unittest.TestCase):
    def test_calculateAngleOfTransmission_normalIncidence(self):
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
        # Given
        coverRefractiveIndex = 2
        substrateRefractiveIndex = np.sqrt(2)
        incidentAngle = np.deg2rad(45)

        # When
        transmissionAngle = el.calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefractiveIndex, incidentAngle
        )

        # Then
        self.assertAlmostEqual(transmissionAngle, np.pi / 2)


if __name__ == "__main__":
    unittest.main()
