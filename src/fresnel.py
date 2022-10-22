import numpy as np


class Senkrecht:
    @staticmethod
    def reflection(
        incidentAngle,
        transmissionAngle,
    ):
        numerator = -1 * np.sin(incidentAngle - transmissionAngle)
        denominator = np.sin(incidentAngle + transmissionAngle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incidentAngle,
        transmissionAngle,
    ):
        numerator = 2 * np.sin(transmissionAngle) * np.cos(incidentAngle)
        denominator = np.sin(incidentAngle + transmissionAngle)
        return numerator / denominator


class Parallel:
    @staticmethod
    def reflection(
        incidentAngle,
        transmissionAngle,
    ):
        numerator = np.tan(incidentAngle - transmissionAngle)
        denominator = np.tan(incidentAngle + transmissionAngle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incidentAngle,
        transmissionAngle,
    ):
        numerator = 2 * np.sin(transmissionAngle) * np.cos(incidentAngle)
        denominator = np.sin(incidentAngle + transmissionAngle) * np.cos(
            incidentAngle - transmissionAngle
        )
        return numerator / denominator
