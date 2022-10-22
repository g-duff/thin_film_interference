'''Calculate ellipsometry parameters psi, delta'''

import functools
import numpy as np
from src.transmission_angles import cascade_transmission_angles
from src.fresnel import Parallel, Senkrecht
from src.optical_path import accumulate_phase
from src.optical_boundary import OpticalBoundary

tau = 2 * np.pi


def ellipsometry(
    free_space_wavelengths,
    illumination_angle,
    film_refractive_indexes,
    film_thicknesses,
    substrate_refractive_index,
    cover_refractive_index=1,
):
    '''Calculate ellipsometry parameters psi, delta from film stack parameters'''

    all_refractive_indexes = [cover_refractive_index] + \
        film_refractive_indexes + [substrate_refractive_index]
    material_refractive_indexes = film_refractive_indexes + \
        [substrate_refractive_index]

    transmitted_angles = cascade_transmission_angles(
        illumination_angle, all_refractive_indexes)

    free_space_wavenumbers = tau / free_space_wavelengths
    wavenumbers_in_layer = [
        ri * free_space_wavenumbers for ri in material_refractive_indexes]

    path_parameters = zip(wavenumbers_in_layer,
                          transmitted_angles, film_thicknesses)
    accumulated_phases = [
        accumulate_phase(*p) for p in path_parameters
    ]

    angle_pairs = pair_parameters(
        illumination_angle, transmitted_angles, transmitted_angles.pop()
    )
    optical_interfaces = [OpticalBoundary(*p) for p in angle_pairs]

    substrate_interface = optical_interfaces.pop()

    for o_i in optical_interfaces + [substrate_interface]:
        o_i.set_polarization(Parallel)

    parallel_reflection = film_stack_response(
        optical_interfaces, accumulated_phases, substrate_interface
    )

    for o_i in optical_interfaces + [substrate_interface]:
        o_i.set_polarization(Senkrecht)

    senkrecht_reflection = film_stack_response(
        optical_interfaces, accumulated_phases, substrate_interface
    )

    return reflection_to_psi_delta(senkrecht_reflection, parallel_reflection)


def pair_parameters(first_item, middle_items, last_item):
    '''Group list of parameters into pairs'''
    return list(
        zip(
            [first_item] + middle_items,
            middle_items + [last_item],
        )
    )


def film_stack_response(
    optical_interfaces,
    accumulated_phases,
    substrate_interface,
):
    '''Reflection from multiple stacked thin films'''
    return functools.reduce(
        lambda reflectionOutOf, opticalProperties: calculate_film_reflection(
            reflectionOutOf,
            opticalProperties[0].reflection_into(),
            opticalProperties[0].transmission_into(),
            opticalProperties[0].transmission_back(),
            opticalProperties[1],
        ),
        zip(optical_interfaces[::-1], accumulated_phases[::-1]),
        substrate_interface.reflection_into(),
    )


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
