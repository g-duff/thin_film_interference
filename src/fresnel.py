import numpy as np


class Senkrecht:
    @staticmethod
    def reflection(
        incidentRefractiveIndex,
        transmissionRefractiveIndex,
        incidentAngle,
        transmissionAngle,
    ):
        numerator = -1 * np.sin(incidentAngle - transmissionAngle)
        denominator = np.sin(incidentAngle + transmissionAngle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incidentRefractiveIndex,
        transmissionRefractiveIndex,
        incidentAngle,
        transmissionAngle,
    ):
        numerator = 2 * incidentRefractiveIndex * np.cos(incidentAngle)
        denominator = incidentRefractiveIndex * np.cos(
            incidentAngle
        ) + transmissionRefractiveIndex * np.cos(transmissionAngle)
        return numerator / denominator


class Parallel:
    @staticmethod
    def reflection(
        incidentRefractiveIndex,
        transmissionRefractiveIndex,
        incidentAngle,
        transmissionAngle,
    ):
        numerator = transmissionRefractiveIndex * np.cos(
            incidentAngle
        ) - incidentRefractiveIndex * np.cos(transmissionAngle)
        denominator = transmissionRefractiveIndex * np.cos(
            incidentAngle
        ) + incidentRefractiveIndex * np.cos(transmissionAngle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incidentRefractiveIndex,
        transmissionRefractiveIndex,
        incidentAngle,
        transmissionAngle,
    ):
        numerator = 2 * incidentRefractiveIndex * np.cos(incidentAngle)
        denominator = transmissionRefractiveIndex * np.cos(
            incidentAngle
        ) + incidentRefractiveIndex * np.cos(transmissionAngle)
        return numerator / denominator
