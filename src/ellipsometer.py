'''Calculate ellipsometry parameters psi, delta'''

import functools
import numpy as np
from src.transmission_angles import propagate_transmission_angles
from src.fresnel import Parallel, Senkrecht
from src.optical_path import OpticalPath
from src.optical_boundary import OpticalBoundary

tau = 2 * np.pi


def ellipsometry(
    free_space_wavelengths,
    incident_angle,
    film_refractive_indexes,
    film_thicknesses,
    substrate_refractive_index,
    cover_refractive_index=1,
):
    '''Calculate ellipsometry parameters psi, delta from film stack parameters'''

    refractive_index_pairs = pairParameters(
        cover_refractive_index, film_refractive_indexes, substrate_refractive_index
    )
    transmitted_angles = propagate_transmission_angles(
        incident_angle, refractive_index_pairs)

    free_space_wavenumbers = tau / free_space_wavelengths
    path_parameters = zip(film_refractive_indexes,
                         film_thicknesses, transmitted_angles)
    accumulated_phases = [
        OpticalPath(*p).accumulate_phase(free_space_wavenumbers) for p in path_parameters
    ]

    angle_pairs = pairParameters(
        incident_angle, transmitted_angles, transmitted_angles.pop()
    )
    optical_interfaces = [OpticalBoundary(*p) for p in angle_pairs]

    substrate_interface = optical_interfaces.pop()

    for o_i in optical_interfaces + [substrate_interface]:
        o_i.set_polarization(Parallel)

    parallel_reflection = filmStackResponse(
        optical_interfaces, accumulated_phases, substrate_interface
    )

    for o_i in optical_interfaces + [substrate_interface]:
        o_i.set_polarization(Senkrecht)

    senkrecht_reflection = filmStackResponse(
        optical_interfaces, accumulated_phases, substrate_interface
    )

    return reflectionToPsiDelta(senkrecht_reflection, parallel_reflection)


def pairParameters(first_item, middle_items, last_item):
    '''Group list of parameters into pairs'''
    return list(
        zip(
            [first_item] + middle_items,
            middle_items + [last_item],
        )
    )


def filmStackResponse(
    optical_interfaces,
    accumulated_phases,
    substrate_interface,
):
    '''Reflection from multiple stacked thin films'''
    return functools.reduce(
        lambda reflectionOutOf, opticalProperties: calculateFilmReflection(
            reflectionOutOf,
            opticalProperties[0].reflection_into(),
            opticalProperties[0].transmission_into(),
            opticalProperties[0].transmission_back(),
            opticalProperties[1],
        ),
        zip(optical_interfaces[::-1], accumulated_phases[::-1]),
        substrate_interface.reflection_into(),
    )


def calculateFilmReflection(
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


def reflectionToPsiDelta(senkrecht_reflection, parallel_reflection):
    '''Convert reflection coefficients to ellipsometry parameters'''
    reflection_ratio = parallel_reflection / senkrecht_reflection
    psi = np.arctan(np.abs(reflection_ratio))
    delta = np.angle(reflection_ratio)
    return psi, delta
