import numpy as np
import matplotlib.pyplot as plt
import thinfilm as tf

# Input

coverRefractiveIndex = 1.0
filmRefractiveIndex = 1.45
substrateRefractiveIndex = 3.8

filmThickness = 800

incidentAngle = 30*tf.degrees

freeSpaceWavelength = np.arange(500, 1000)

# Angles
rayAngleInFilm = tf.calculateTransmissionAngle(coverRefractiveIndex, filmRefractiveIndex, incidentAngle)
transmissionAngle = tf.calculateTransmissionAngle(filmRefractiveIndex, substrateRefractiveIndex, rayAngleInFilm)

# Fresnel coefficients for both polarisations

fresnelSenkrechtCoefficients = {
    'reflectionInto': tf.calculateSenkrechtReflection(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, rayAngleInFilm),
    'reflectionOutOf': tf.calculateSenkrechtReflection(filmRefractiveIndex, substrateRefractiveIndex, rayAngleInFilm, transmissionAngle),
    'transmissionInto': tf.calculateSenkrechtTransmission(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, rayAngleInFilm),
    'transmissionBack': tf.calculateSenkrechtTransmission(filmRefractiveIndex, coverRefractiveIndex, rayAngleInFilm, incidentAngle),
}

fresnelParallelCoefficients = {
    'reflectionInto': tf.calculateParallelReflection(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, rayAngleInFilm),
    'reflectionOutOf': tf.calculateParallelReflection(filmRefractiveIndex, substrateRefractiveIndex, rayAngleInFilm, transmissionAngle),
    'transmissionInto': tf.calculateParallelTransmission(coverRefractiveIndex, filmRefractiveIndex, incidentAngle, rayAngleInFilm),
    'transmissionBack': tf.calculateParallelTransmission(filmRefractiveIndex, coverRefractiveIndex, rayAngleInFilm, incidentAngle),
}

# Phase difference from rays

freeSpaceWavenumber = 2*np.pi/freeSpaceWavelength
phaseDifference = tf.calculatePhaseDifference(freeSpaceWavenumber, rayAngleInFilm, filmRefractiveIndex, filmThickness)

# Multiple beam interference in Fabry Perot cavity

senkrechtReflection = tf.calculateFilmReflection(phaseDifference,  **fresnelSenkrechtCoefficients)
parallelReflection = tf.calculateFilmReflection(phaseDifference,  **fresnelParallelCoefficients)

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
