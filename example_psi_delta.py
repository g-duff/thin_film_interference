import numpy as np
import matplotlib.pyplot as plt
import src.ellipsometerService as el

# Input

filmRefractiveIndices = [3.8, 1.45]
filmThicknesses = [220, 3000]

incidentAngle = 65*el.degrees

freeSpaceWavelength = np.arange(500, 1000)

# Calculation

psi, delta = el.ellipsometry(freeSpaceWavelength, incidentAngle, filmRefractiveIndices, filmThicknesses, 3.8)

# Graphical output

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.set_title(r'tan$(\Psi$)')
ax1.plot(freeSpaceWavelength, np.tan(psi))

ax2.set_title(r'cos$(\Delta$)')
ax2.plot(freeSpaceWavelength, np.cos(delta))

ax2.set_xlabel('Free space wavelength (nm)')

fig.tight_layout()

fig.savefig('./example_figures/psi_delta.png')

plt.show()
