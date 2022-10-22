import numpy as np
import matplotlib.pyplot as plt
import src.ellipsometer as el
from src.optical_boundary import OpticalBoundary
from src.optical_path import OpticalPath
from src.fresnel import Parallel, Senkrecht

coverRefractiveIndex = 1.0
filmRefractiveIndex = 1.45
substrateRefractiveIndex = 3.8
filmThickness = 800
incidentAngle = np.deg2rad(30)
freeSpaceWavelength = np.arange(500, 1000)

rayAngleInFilm = el.calculateTransmissionAngle(
    coverRefractiveIndex, filmRefractiveIndex, incidentAngle
)
transmissionAngle = el.calculateTransmissionAngle(
    filmRefractiveIndex, substrateRefractiveIndex, rayAngleInFilm
)

upperInterface = OpticalBoundary(
    incidentAngle, rayAngleInFilm
)
lowerInterface = OpticalBoundary(
    rayAngleInFilm, transmissionAngle
)

freeSpaceWavenumber = 2 * np.pi / freeSpaceWavelength
phaseDifference = OpticalPath(
    filmRefractiveIndex, filmThickness, rayAngleInFilm
).accumulate_phase(freeSpaceWavenumber)

upperInterface.set_polarization(Senkrecht)
lowerInterface.set_polarization(Senkrecht)
senkrechtReflection = el.calculateFilmReflection(
    lowerInterface.reflection_into(),
    upperInterface.reflection_into(),
    upperInterface.transmission_into(),
    upperInterface.transmission_back(),
    phaseDifference,
)

lowerInterface.set_polarization(Parallel)
upperInterface.set_polarization(Parallel)
parallelReflection = el.calculateFilmReflection(
    lowerInterface.reflection_into(),
    upperInterface.reflection_into(),
    upperInterface.transmission_into(),
    upperInterface.transmission_back(),
    phaseDifference,
)

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.set_title("S polarisation")
ax1.set_ylabel("Reflectance")
ax1.plot(freeSpaceWavelength, np.abs(senkrechtReflection) ** 2)

ax2.set_title("P polarisation")
ax2.set_ylabel("Reflectance")
ax2.plot(freeSpaceWavelength, np.abs(parallelReflection) ** 2)

ax2.set_xlabel("Free space wavelength (nm)")

fig.tight_layout()

fig.savefig("./example_figures/fabryperot_single.png")

plt.show()
