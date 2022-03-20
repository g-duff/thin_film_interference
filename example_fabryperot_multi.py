import numpy as np
import matplotlib.pyplot as plt
import ellipsometer as el

# Input

coverRefractiveIndex = 1.0
substrateRefractiveIndices = [3.8, 1.45, 3.8]
filmThicknesses = [220, 2000]

incidentAngle = 30*el.degrees

freeSpaceWavelength = np.arange(500, 1000)

# Calculation
freeSpaceWavenumber = 2*np.pi/freeSpaceWavelength

substrateRefractiveIndices.reverse()
filmThicknesses.reverse()

r_s = el.nextLayerSenkrechtReflection(freeSpaceWavenumber, incidentAngle, coverRefractiveIndex, substrateRefractiveIndices[:], filmThicknesses[:])
r_p = el.nextLayerParallelReflection(freeSpaceWavenumber, incidentAngle, coverRefractiveIndex, substrateRefractiveIndices[:], filmThicknesses[:])

# Graphical output

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.set_title('S polarisation')
ax1.set_ylabel('Reflectance')
ax1.plot(freeSpaceWavelength, np.abs(r_s)**2)

ax2.set_title('P polarisation')
ax2.set_ylabel('Reflectance')
ax2.plot(freeSpaceWavelength, np.abs(r_p)**2)

ax2.set_xlabel('Free space wavelength (nm)')

fig.tight_layout()

fig.savefig('./example_figures/fabryperot_multi.png')

plt.show()
