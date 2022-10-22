'''Optical Interface calculations'''

class OpticalBoundary:
    '''Optical Interface class, encapsulating Fresnel coefficients'''
    def __init__(self, refractiveIndexPair, rayAnglePair):
        self.refractiveIndexPair = refractiveIndexPair
        self.rayAnglePair = rayAnglePair

    def set_polarization(self, Polarization):
        '''Set polarization for reflection and transmission calculations'''
        self.Polarization = Polarization

    def reflection_into(self):
        '''Calculate reflection towards the interface'''
        return self.Polarization.reflection(
            *self.rayAnglePair,
        )

    def transmission_into(self):
        '''Calculate transmission through the interface'''
        return self.Polarization.transmission(
            *self.rayAnglePair,
        )

    def transmission_back(self):
        '''Calculate transmission back through interface'''
        return self.Polarization.transmission(
            *self.rayAnglePair[::-1],
        )
