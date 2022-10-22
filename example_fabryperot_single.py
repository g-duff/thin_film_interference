import numpy as np
import matplotlib.pyplot as plt
import src.ellipsometerService as el
from src.optical_boundary import OpticalInterface
from src.opticalPathDomain import OpticalPath
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

upperInterface = OpticalInterface(
    (coverRefractiveIndex, filmRefractiveIndex), (incidentAngle, rayAngleInFilm)
)
lowerInterface = OpticalInterface(
    (filmRefractiveIndex, substrateRefractiveIndex), (rayAngleInFilm, transmissionAngle)
)

freeSpaceWavenumber = 2 * np.pi / freeSpaceWavelength
phaseDifference = OpticalPath(
    filmRefractiveIndex, filmThickness, rayAngleInFilm
).accumulatePhase(freeSpaceWavenumber)

upperInterface.setPolarization(Senkrecht)
lowerInterface.setPolarization(Senkrecht)
senkrechtReflection = el.calculateFilmReflection(
    lowerInterface.reflectionInto(),
    upperInterface.reflectionInto(),
    upperInterface.transmissionInto(),
    upperInterface.transmissionBack(),
    phaseDifference,
)

lowerInterface.setPolarization(Parallel)
upperInterface.setPolarization(Parallel)
parallelReflection = el.calculateFilmReflection(
    lowerInterface.reflectionInto(),
    upperInterface.reflectionInto(),
    upperInterface.transmissionInto(),
    upperInterface.transmissionBack(),
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
