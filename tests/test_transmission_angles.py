import src.transmission_angles as ta
import unittest
import numpy as np


class transmissionAngles(unittest.TestCase):
    def test_calculateAngleOfTransmission_normalIncidence(self):
        # Given
        coverRefractiveIndex = 1.0
        substrateRefractiveIndex = 1.5
        incidentAngle = 0

        # When
        transmissionAngle = ta.calculateTransmissionAngle(
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
        transmissionAngle = ta.calculateTransmissionAngle(
            coverRefractiveIndex, substrateRefractiveIndex, incidentAngle
        )

        # Then
        self.assertAlmostEqual(transmissionAngle, np.pi / 2)

    def test_propagateTransmissionAngles_symmetricStack(self):
        # Given
        coverRefractiveIndex = 2
        substrateRefractiveIndices = [
            (coverRefractiveIndex, np.sqrt(2)),
            (np.sqrt(2), coverRefractiveIndex),
        ]
        incidentAngle = np.deg2rad(45)

        # When
        transmissionAngles = ta.propagateTransmissionAngles(
            incidentAngle, substrateRefractiveIndices
        )

        # Then
        diff = sum(
            (angle1 - angle2) ** 2
            for angle1, angle2 in zip(transmissionAngles, [np.pi / 2, incidentAngle])
        )
        self.assertAlmostEqual(diff, 0)
        self.assertAlmostEqual(transmissionAngles[-1], incidentAngle)


if __name__ == "__main__":
    unittest.main()
