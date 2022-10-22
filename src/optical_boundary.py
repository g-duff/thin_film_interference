'''Optical Interface calculations'''


class OpticalBoundary:
    '''Optical Interface class, encapsulating Fresnel coefficients'''

    def __init__(self, incident_ray_angle, transmitted_ray_angle):
        self.incident_ray_angle = incident_ray_angle
        self.transmitted_ray_angle = transmitted_ray_angle
        self.polarization = None

    def set_polarization(self, polarization):
        '''Set polarization for reflection and transmission calculations'''
        self.polarization = polarization

    def reflection_into(self):
        '''Calculate reflection towards the interface'''
        return self.polarization.reflection(
            self.incident_ray_angle,
            self.transmitted_ray_angle
        )

    def transmission_into(self):
        '''Calculate transmission through the interface'''
        return self.polarization.transmission(
            self.incident_ray_angle,
            self.transmitted_ray_angle
        )

    def transmission_back(self):
        '''Calculate transmission back through interface'''
        return self.polarization.transmission(
            self.transmitted_ray_angle,
            self.incident_ray_angle
        )
