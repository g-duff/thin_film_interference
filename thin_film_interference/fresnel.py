'''Fresnel reflection and transmission coefficients'''


class Senkrecht:
    '''Senkrecht, or Perpendicular polarization'''
    @staticmethod
    def reflection(
            incident_wavevector_normal_component: float,
            transmission_wavevector_normal_component: float,
    ) -> float:
        '''Calculate Senkrecht reflection coefficient
        at a flat interface, from normal components of wavevectors.

        Parameters
        ----------
        incident_wavevector_normal_component: float
        transmission_wavevector_normal_component: float

        Returns
        -------
        reflection coefficient: float
        '''
        numerator = incident_wavevector_normal_component - \
            transmission_wavevector_normal_component
        denominator = incident_wavevector_normal_component + \
            transmission_wavevector_normal_component
        return numerator / denominator

    @staticmethod
    def transmission(
            incident_wavevector_normal_component: float,
            transmission_wavevector_normal_component: float,
    ) -> float:
        '''Calculate Senkrecht transmission coefficient
        at a flat interface, from normal components of wavevectors.

        Parameters
        ----------
        incident_wavevector_normal_component: float
        transmission_wavevector_normal_component: float

        Returns
        -------
        transmission coefficient: float
        '''
        numerator = 2 * incident_wavevector_normal_component
        denominator = incident_wavevector_normal_component + \
            transmission_wavevector_normal_component
        return numerator / denominator


class Parallel:
    '''Parallel polarization'''
    @staticmethod
    def reflection(
            incident_wavevector_normal_component: float,
            transmission_wavevector_normal_component: float,
            incident_refractive_index: float,
            transmission_refractive_index: float,
    ) -> float:
        '''Calculate Parallel reflection coefficient
        at a flat interface, from normal components of wavevectors.

        Parameters
        ----------
        incident_wavevector_normal_component: float
        transmission_wavevector_normal_component: float
        incident_refractive_index: float
        transmission_refractive_index: float


        Returns
        -------
        reflection coefficient: float
        '''
        numerator = incident_wavevector_normal_component * transmission_refractive_index**2 - \
            transmission_wavevector_normal_component * incident_refractive_index**2
        denominator = incident_wavevector_normal_component * transmission_refractive_index**2 + \
            transmission_wavevector_normal_component * incident_refractive_index**2
        return numerator / denominator

    @staticmethod
    def transmission(
            incident_wavevector_normal_component: float,
            transmission_wavevector_normal_component: float,
            incident_refractive_index: float,
            transmission_refractive_index: float,
    ) -> float:
        '''Calculate Parallel transmission coefficient
        at a flat interface, from normal components of wavevectors.

        Parameters
        ----------
        incident_wavevector_normal_component: float
        transmission_wavevector_normal_component: float
        incident_refractive_index: float
        transmission_refractive_index: float


        Returns
        -------
        transmission coefficient: float
        '''
        numerator = 2 * incident_wavevector_normal_component * \
            incident_refractive_index * transmission_refractive_index
        denominator = incident_wavevector_normal_component * transmission_refractive_index**2 + \
            transmission_wavevector_normal_component * incident_refractive_index**2
        return numerator / denominator
