# Thin Film Interference

## Features

* Ellipsometry parameters psi and delta
* Arbitrary number of layers
* All-numpy implementation

![image](./example_figures/psi_delta.png)

# Usage

Interface:
```py
def ellipsometry(free_space_wavelengths: list | np.array,
    illumination_angle: float,
    refractive_indexes: list | np.array,
    film_thicknesses: list | np.array) -> (psi, delta)
```

Example function call:
```py
cover_refractive_index = 1.0
substrate_refractive_index = 3.8
refractive_indices = [cover_refractive_index, 3.8, 1.45, substrate_refractive_index]
film_thicknesses = [220, 3000]
incident_angle = np.deg2rad(65)

psi, delta = ellipsometry(
    free_space_wavelength,
    incident_angle,
    refractive_indices,
    film_thicknesses,
)
```
