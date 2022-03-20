import numpy as np
import matplotlib.pyplot as plt
import ellipsometer as el

# Input

coverRefractiveIndex = 1.0
filmRefractiveIndex = 1.45
substrateRefractiveIndex = 3.8

filmThickness = 800

incidentAngle = 30*el.degrees

freeSpaceWavelength = np.arange(500, 1000)

# Angles
rayAngleInFilm = el.calculateTransmissionAngle(coverRefractiveIndex, filmRefractiveIndex, incidentAngle)
transmissionAngle = el.calculateTransmissionAngle(filmRefractiveIndex, substrateRefractiveIndex, rayAngleInFilm)

# Fresnel coefficients for both polarisations

fresnelSenkrechtCoefficients = {
    'reflectionInto': el.calculateSenkrechtReflection(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, rayAngleInFilm),
    'reflectionOutOf': el.calculateSenkrechtReflection(filmRefractiveIndex, substrateRefractiveIndex, rayAngleInFilm, transmissionAngle),
    'transmissionInto': el.calculateSenkrechtTransmission(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, rayAngleInFilm),
    'transmissionBack': el.calculateSenkrechtTransmission(filmRefractiveIndex, coverRefractiveIndex, rayAngleInFilm, incidentAngle),
}

fresnelParallelCoefficients = {
    'reflectionInto': el.calculateParallelReflection(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, rayAngleInFilm),
    'reflectionOutOf': el.calculateParallelReflection(filmRefractiveIndex, substrateRefractiveIndex, rayAngleInFilm, transmissionAngle),
    'transmissionInto': el.calculateParallelTransmission(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, rayAngleInFilm),
    'transmissionBack': el.calculateParallelTransmission(filmRefractiveIndex, coverRefractiveIndex, rayAngleInFilm, incidentAngle),
}

# Phase difference from rays

freeSpaceWavenumber = 2*np.pi/freeSpaceWavelength
phaseDifference = el.calculatePhaseDifference(freeSpaceWavenumber, rayAngleInFilm, filmRefractiveIndex, filmThickness)

# Multiple beam interference in Fabry Perot cavity

senkrechtReflection = el.calculateFilmReflection(phaseDifference,  **fresnelSenkrechtCoefficients)
parallelReflection = el.calculateFilmReflection(phaseDifference,  **fresnelParallelCoefficients)

# Graphical output

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.set_title('S polarisation')
ax1.set_ylabel('Reflectance')
ax1.plot(freeSpaceWavelength, np.abs(senkrechtReflection)**2)

ax2.set_title('P polarisation')
ax2.set_ylabel('Reflectance')
ax2.plot(freeSpaceWavelength, np.abs(parallelReflection)**2)

ax2.set_xlabel('Free space wavelength (nm)')

fig.tight_layout()

fig.savefig('./example_figures/fabryperot_single.png')

plt.show()
