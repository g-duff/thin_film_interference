# pylint: disable = import-error, missing-class-docstring, missing-function-docstring, missing-module-docstring
import unittest
import numpy as np
import src.transmission_angles as ta


class TransmissionAngles(unittest.TestCase):
    def test_transmission_angle_normal_incidence(self):
        # Given
        cover_refractive_index = 1.0
        substrate_refractive_index = 1.5
        incident_angle = 0

        # When
        transmission_angle = ta.calculate_transmission_angle(
            cover_refractive_index, substrate_refractive_index, incident_angle
        )

        # Then
        self.assertEqual(transmission_angle, 0)

    def test_calculate_transmission_angle_oblique_incidence(self):
        # Given
        cover_refractive_index = 2
        substrate_refractive_index = np.sqrt(2)
        incident_angle = np.deg2rad(45)

        # When
        transmission_angle = ta.calculate_transmission_angle(
            cover_refractive_index, substrate_refractive_index, incident_angle
        )

        # Then
        self.assertAlmostEqual(transmission_angle, np.pi / 2)

    def test_propagatetransmission_angles_symmetric_stack(self):
        # Given
        cover_refractive_index = 2
        substrate_refractive_indices = [
            cover_refractive_index, np.sqrt(2), cover_refractive_index,
        ]
        incident_angle = np.deg2rad(45)

        # When
        transmission_angles = ta.propagate_transmission_angles(
            incident_angle, substrate_refractive_indices
        )

        # Then
        diff = sum(
            (angle1 - angle2) ** 2
            for angle1, angle2 in zip(transmission_angles, [np.pi / 2, incident_angle])
        )
        self.assertAlmostEqual(diff, 0)
        self.assertAlmostEqual(transmission_angles[-1], incident_angle)


if __name__ == "__main__":
    unittest.main()
