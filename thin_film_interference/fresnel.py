'''Fresnel reflection and transmission coefficients'''


class Senkrecht:
    '''Senkrecht, or Perpendicular polarization'''
    @staticmethod
    def reflection(
        incident_wavevector_normal_component,
        transmission_wavevector_normal_component,
    ):
        '''Calculate reflection coefficient'''
        numerator = incident_wavevector_normal_component - \
            transmission_wavevector_normal_component
        denominator = incident_wavevector_normal_component + \
            transmission_wavevector_normal_component
        return numerator / denominator

    @staticmethod
    def transmission(
        incident_wavevector_normal_component,
        transmission_wavevector_normal_component,
    ):
        '''Calculate transmission coefficient'''
        numerator = 2 * incident_wavevector_normal_component
        denominator = incident_wavevector_normal_component + \
            transmission_wavevector_normal_component
        return numerator / denominator


class Parallel:
    '''Parallel polarization'''
    @staticmethod
    def reflection(
        incident_wavevector_normal_component,
        transmission_wavevector_normal_component,
        incident_refractive_index,
        transmission_refractive_index,
    ):
        '''Calculate reflection coefficient'''
        numerator = incident_wavevector_normal_component * transmission_refractive_index**2 - \
            transmission_wavevector_normal_component * incident_refractive_index**2
        denominator = incident_wavevector_normal_component * transmission_refractive_index**2 + \
            transmission_wavevector_normal_component * incident_refractive_index**2
        return numerator / denominator

    @staticmethod
    def transmission(
        incident_wavevector_normal_component,
        transmission_wavevector_normal_component,
        incident_refractive_index,
        transmission_refractive_index,
    ):
        '''Calculate transmission coefficient'''
        numerator = 2 * incident_wavevector_normal_component * \
            incident_refractive_index * transmission_refractive_index
        denominator = incident_wavevector_normal_component * transmission_refractive_index**2 + \
            transmission_wavevector_normal_component * incident_refractive_index**2
        return numerator / denominator
