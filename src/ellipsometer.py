'''Calculate ellipsometry parameters psi, delta'''

import numpy as np
from src.transmission_angles import cascade_transmission_angles
from src.fresnel import Parallel, Senkrecht


def ellipsometry(
    free_space_wavelengths,
    illumination_angle,
    refractive_indexes,
    film_thicknesses,
):
    '''Calculate ellipsometry parameters psi, delta from film stack parameters'''

    all_angles = [illumination_angle] + cascade_transmission_angles(
        illumination_angle, refractive_indexes)

    wavevector_normal_components = [n*np.cos(angle) * 2 * np.pi / free_space_wavelengths
                                    for n, angle in zip(refractive_indexes, all_angles)]

    senkrecht_reflection = Senkrecht.reflection(
        wavevector_normal_components[-2], wavevector_normal_components[-1])
    parallel_reflection = Parallel.reflection(
        wavevector_normal_components[-2], wavevector_normal_components[-1],
        refractive_indexes[-2], refractive_indexes[-1])

    sample_parameters = zip(
        refractive_indexes[-3::-1],
        wavevector_normal_components[-3::-1],
        refractive_indexes[-2::-1],
        wavevector_normal_components[-2::-1],
        film_thicknesses[::-1],
    )

    for incident_refractive_index, incident_wavevector_normal_component, layer_refractive_index, layer_wavevector_normal_component, layer_thickness in sample_parameters:

        accumulated_phase = 2 * layer_thickness * layer_wavevector_normal_component
        parallel_reflection = calculate_film_reflection(
            reflection_out_of=parallel_reflection,
            reflection_into=Parallel.reflection(
                incident_wavevector_normal_component, layer_wavevector_normal_component,
                incident_refractive_index, layer_refractive_index),
            transmission_into=Parallel.transmission(
                incident_wavevector_normal_component, layer_wavevector_normal_component,
                incident_refractive_index, layer_refractive_index),
            transmission_back=Parallel.transmission(  # pylint: disable = arguments-out-of-order
                layer_wavevector_normal_component, incident_wavevector_normal_component,
                layer_refractive_index, incident_refractive_index),
            accumulated_phase=accumulated_phase
        )
        senkrecht_reflection = calculate_film_reflection(
            reflection_out_of=senkrecht_reflection,
            reflection_into=Senkrecht.reflection(
                incident_wavevector_normal_component, layer_wavevector_normal_component),
            transmission_into=Senkrecht.transmission(
                incident_wavevector_normal_component, layer_wavevector_normal_component),
            transmission_back=Senkrecht.transmission(  # pylint: disable = arguments-out-of-order
                layer_wavevector_normal_component, incident_wavevector_normal_component),
            accumulated_phase=accumulated_phase
        )

    return reflection_to_psi_delta(senkrecht_reflection, parallel_reflection)


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
