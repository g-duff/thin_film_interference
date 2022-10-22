# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
import src.transmission_angles as ta


class transmissionAngles(unittest.TestCase):
    def test_calculateAngleOfTransmission_normalIncidence(self):
        # Given
        coverRefractiveIndex = 1.0
        substrateRefractiveIndex = 1.5
        incidentAngle = 0

        # When
        transmissionAngle = ta.calculate_transmission_angle(
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
        transmissionAngle = ta.calculate_transmission_angle(
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
        transmissionAngles = ta.propagate_transmission_angles(
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
