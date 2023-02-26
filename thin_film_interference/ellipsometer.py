'''Calculate ellipsometry parameters psi, delta'''

from itertools import tee
import numpy as np
from .fresnel import Parallel, Senkrecht


def ellipsometry(
    free_space_wavelengths,
    illumination_angle,
    refractive_indexes,
    film_thicknesses,
):
    '''Calculate ellipsometry parameters psi, delta from film stack parameters'''

    refractive_indexes.reverse()
    film_thicknesses.reverse()

    free_space_wavevectors = 2 * np.pi / free_space_wavelengths
    wavevector_normal_components = [free_space_wavevectors * np.sqrt(
        n**2 - (np.sin(illumination_angle) * refractive_indexes[-1])**2)
        for n in refractive_indexes]

    senkrecht_reflection = Senkrecht.reflection(
        wavevector_normal_components[1], wavevector_normal_components[0])
    parallel_reflection = Parallel.reflection(
        wavevector_normal_components[1], wavevector_normal_components[0],
        refractive_indexes[1], refractive_indexes[0])

    waves = pairwise(
        zip(refractive_indexes[1::], wavevector_normal_components[1::])
    )

    for (wave_in_film, incident_wave), layer_thickness in zip(waves, film_thicknesses):

        film_refractive_index, film_wavevector_normal_component = wave_in_film
        incident_refractive_index, incident_wavevector_normal_component = incident_wave

        accumulated_phase = 2 * layer_thickness * film_wavevector_normal_component
        parallel_reflection = calculate_film_reflection(
            reflection_out_of=parallel_reflection,
            reflection_into=Parallel.reflection(
                incident_wavevector_normal_component, film_wavevector_normal_component,
                incident_refractive_index, film_refractive_index),
            transmission_into=Parallel.transmission(
                incident_wavevector_normal_component, film_wavevector_normal_component,
                incident_refractive_index, film_refractive_index),
            transmission_back=Parallel.transmission(  # pylint: disable = arguments-out-of-order
                film_wavevector_normal_component, incident_wavevector_normal_component,
                film_refractive_index, incident_refractive_index),
            accumulated_phase=accumulated_phase
        )
        senkrecht_reflection = calculate_film_reflection(
            reflection_out_of=senkrecht_reflection,
            reflection_into=Senkrecht.reflection(
                incident_wavevector_normal_component, film_wavevector_normal_component),
            transmission_into=Senkrecht.transmission(
                incident_wavevector_normal_component, film_wavevector_normal_component),
            transmission_back=Senkrecht.transmission(  # pylint: disable = arguments-out-of-order
                film_wavevector_normal_component, incident_wavevector_normal_component),
            accumulated_phase=accumulated_phase
        )

    return reflection_to_psi_delta(senkrecht_reflection, parallel_reflection)


def pairwise(iterable):
    ''' pairwise('ABCDEFG') --> AB BC CD DE EF FG'''
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def calculate_film_reflection(
    reflection_out_of,
    reflection_into,
    transmission_into,
    transmission_back,
    accumulated_phase,
):
    '''Reflection from single thin film'''
    numerator = transmission_into * reflection_out_of * transmission_back
    demoninator = np.exp(-1j * accumulated_phase) + \
        reflection_into * reflection_out_of
    return reflection_into + numerator / demoninator


def reflection_to_psi_delta(senkrecht_reflection, parallel_reflection):
    '''Convert reflection coefficients to ellipsometry parameters'''
    reflection_ratio = parallel_reflection / senkrecht_reflection
    psi = np.arctan(np.abs(reflection_ratio))
    delta = np.angle(reflection_ratio)
    return psi, delta
