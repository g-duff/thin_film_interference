'''Calculate ellipsometry parameters psi, delta'''

import numpy as np
from src.transmission_angles import cascade_transmission_angles
from src.fresnel import Parallel, Senkrecht
from src.optical_path import accumulate_phase

tau = 2 * np.pi


def ellipsometry(
    free_space_wavelengths,
    illumination_angle,
    refractive_indexes,
    film_thicknesses,
):
    '''Calculate ellipsometry parameters psi, delta from film stack parameters'''

    transmitted_angles = cascade_transmission_angles(
        illumination_angle, refractive_indexes)

    wavenumbers_in_layer = [
        tau * ri * free_space_wavelengths for ri in refractive_indexes]

    last_trasmission_angle = transmitted_angles.pop()
    senkrecht_reflection = Senkrecht.reflection(
        transmitted_angles[-1], last_trasmission_angle)
    parallel_reflection = Parallel.reflection(
        transmitted_angles[-1], last_trasmission_angle)

    sample_parameters = zip(wavenumbers_in_layer[::-1],
                            film_thicknesses[::-1],
                            transmitted_angles[-1::-1],
                            transmitted_angles[-2::-1] + [illumination_angle]
                            )

    for wavenumber, thickness, ray_angle_in_layer, incident_ray_angle in sample_parameters:
        accumulated_phase = accumulate_phase(
            wavenumber, ray_angle_in_layer, thickness)
        parallel_reflection = calculate_film_reflection(
            reflection_out_of=parallel_reflection,
            reflection_into=Parallel.reflection(
                incident_ray_angle, ray_angle_in_layer),
            transmission_into=Parallel.transmission(
                incident_ray_angle, ray_angle_in_layer),
            transmission_back=Parallel.transmission(
                ray_angle_in_layer, incident_ray_angle),
            accumulated_phase=accumulated_phase
        )
        senkrecht_reflection = calculate_film_reflection(
            reflection_out_of=senkrecht_reflection,
            reflection_into=Senkrecht.reflection(
                incident_ray_angle, ray_angle_in_layer),
            transmission_into=Senkrecht.transmission(
                incident_ray_angle, ray_angle_in_layer),
            transmission_back=Senkrecht.transmission(
                ray_angle_in_layer, incident_ray_angle),
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
    demoninator = np.exp(-1j * 2 * accumulated_phase) + \
        reflection_into * reflection_out_of
    return reflection_into + numerator / demoninator


def reflection_to_psi_delta(senkrecht_reflection, parallel_reflection):
    '''Convert reflection coefficients to ellipsometry parameters'''
    reflection_ratio = parallel_reflection / senkrecht_reflection
    psi = np.arctan(np.abs(reflection_ratio))
    delta = np.angle(reflection_ratio)
    return psi, delta
