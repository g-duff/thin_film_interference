from numpy import cos


class Senkrecht:
    @staticmethod
    def reflection(
        incidentRefractiveIndex,
        transmissionRefractiveIndex,
        incidentAngle,
        transmissionAngle,
    ):
        numerator = incidentRefractiveIndex * cos(
            incidentAngle
        ) - transmissionRefractiveIndex * cos(transmissionAngle)
        denominator = incidentRefractiveIndex * cos(
            incidentAngle
        ) + transmissionRefractiveIndex * cos(transmissionAngle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incidentRefractiveIndex,
        transmissionRefractiveIndex,
        incidentAngle,
        transmissionAngle,
    ):
        numerator = 2 * incidentRefractiveIndex * cos(incidentAngle)
        denominator = incidentRefractiveIndex * cos(
            incidentAngle
        ) + transmissionRefractiveIndex * cos(transmissionAngle)
        return numerator / denominator


class Parallel:
    @staticmethod
    def reflection(
        incidentRefractiveIndex,
        transmissionRefractiveIndex,
        incidentAngle,
        transmissionAngle,
    ):
        numerator = transmissionRefractiveIndex * cos(
            incidentAngle
        ) - incidentRefractiveIndex * cos(transmissionAngle)
        denominator = transmissionRefractiveIndex * cos(
            incidentAngle
        ) + incidentRefractiveIndex * cos(transmissionAngle)
        return numerator / denominator

    @staticmethod
    def transmission(
        incidentRefractiveIndex,
        transmissionRefractiveIndex,
        incidentAngle,
        transmissionAngle,
    ):
        numerator = 2 * incidentRefractiveIndex * cos(incidentAngle)
        denominator = transmissionRefractiveIndex * cos(
            incidentAngle
        ) + incidentRefractiveIndex * cos(transmissionAngle)
        return numerator / denominator
