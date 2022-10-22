class OpticalInterface:
    def __init__(self, refractiveIndexPair, rayAnglePair):
        self.refractiveIndexPair = refractiveIndexPair
        self.rayAnglePair = rayAnglePair

    def setPolarization(self, Polarization):
        self.Polarization = Polarization

    def reflectionInto(self):
        return self.Polarization.reflection(
            *self.rayAnglePair,
        )

    def transmissionInto(self):
        return self.Polarization.transmission(
            *self.rayAnglePair,
        )

    def transmissionBack(self):
        return self.Polarization.transmission(
            *self.rayAnglePair[::-1],
        )
