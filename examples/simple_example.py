''' thin_film_interference calculates psi and delta for constant refractive indices.'''
import numpy as np
import matplotlib.pyplot as plt
from thin_film_interference.ellipsometer import ellipsometry


if __name__ == '__main__':
    free_space_wavelength_in_microns: np.array = np.arange(0.5, 1.0, 0.001)

    substrate_refractive_index = 3.8
    cover_refractive_index = 1.0
    refractive_indices = [cover_refractive_index] + \
        [3.8, 1.45] + [substrate_refractive_index]
    film_thicknesses = [0.22, 3.0]
    incident_angle = np.deg2rad(65)

    # When
    psi, delta = ellipsometry(
        free_space_wavelength_in_microns,
        incident_angle,
        refractive_indices,
        film_thicknesses,
    )

    fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

    ax1.set_title(r"tan$(\Psi$)")
    ax1.plot(free_space_wavelength_in_microns, np.tan(
        psi), label="constant refractive index")

    ax2.set_title(r"cos$(\Delta$)")
    ax2.plot(free_space_wavelength_in_microns, np.cos(
        delta), label="constant refractive index")

    ax2.set_xlabel(r"Free space wavelength $(\mu m)$")

    fig.tight_layout()
    plt.savefig('figures/psi_delta.png')
