''' thin_film_interference calculates psi and delta for constant and varying refractive indices.'''
import numpy as np
import matplotlib.pyplot as plt
from thin_film_interference.ellipsometer import ellipsometry


def cauchy_dispersion_relation(wavelength: np.array, A, B) -> np.array:
    '''Simple Cauchy dispersion relation, taken from Wikipedia
    Taken from wikipedia: https://en.wikipedia.org/wiki/Cauchy%27s_equation'''
    return A + B/wavelength**2


if __name__ == '__main__':
    free_space_wavelength_in_microns: np.array = np.arange(0.5, 1.0, 0.001)
    film_thicknesses_in_microns = [2]

    # Taken from wikipedia: https://en.wikipedia.org/wiki/Cauchy%27s_equation
    dispersive_silica_refractive_index: np.array = cauchy_dispersion_relation(
        free_space_wavelength_in_microns, 1.458, 0.003584)

    constant_silica_refractive_index: float = 1.458

    cover_refractive_index: float = 1.0
    substrate_refractive_index: float = 3.8

    constant_refractive_indices: 'list[float|np.array]' = [
        cover_refractive_index, constant_silica_refractive_index, substrate_refractive_index]
    dispersive_refractive_indices: 'list[float|np.array]' = [
        cover_refractive_index, dispersive_silica_refractive_index, substrate_refractive_index]

    incident_angle_in_radians = np.deg2rad(65)

    constant_silica_psi, constant_silica_delta = ellipsometry(
        free_space_wavelength_in_microns,
        incident_angle_in_radians,
        constant_refractive_indices,
        film_thicknesses_in_microns,
    )

    dispersive_silica_psi, dispersive_silica_delta = ellipsometry(
        free_space_wavelength_in_microns,
        incident_angle_in_radians,
        dispersive_refractive_indices,
        film_thicknesses_in_microns,
    )

    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

    ax1.set_title(r"tan$(\Psi$)")
    ax1.plot(free_space_wavelength_in_microns, np.tan(
        constant_silica_psi), label="constant refractive index")
    ax1.plot(free_space_wavelength_in_microns, np.tan(
        dispersive_silica_psi), label="dispersive medium")
    ax1.legend()

    ax2.set_title(r"cos$(\Delta$)")
    ax2.plot(free_space_wavelength_in_microns, np.cos(
        constant_silica_delta), label="constant refractive index")
    ax2.plot(free_space_wavelength_in_microns, np.cos(
        dispersive_silica_delta), label="dispersive medium")
    ax2.legend()

    ax2.set_xlabel(r"Free space wavelength $(\mu m)$")

    fig.tight_layout()

    plt.show()

