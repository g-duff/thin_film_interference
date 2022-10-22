import numpy as np
import matplotlib.pyplot as plt
import src.ellipsometer as el

filmThicknesses = [220, 3000]
filmRefractiveIndices = [3.8, 1.45]
substrateRefractivIndex = 3.8
incidentAngle = np.deg2rad(65)
freeSpaceWavelength = np.arange(500, 1000)

psi, delta = el.ellipsometry(
    freeSpaceWavelength,
    incidentAngle,
    filmRefractiveIndices,
    filmThicknesses,
    substrateRefractivIndex,
)

fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)

ax1.set_title(r"tan$(\Psi$)")
ax1.plot(freeSpaceWavelength, np.tan(psi))

ax2.set_title(r"cos$(\Delta$)")
ax2.plot(freeSpaceWavelength, np.cos(delta))

ax2.set_xlabel("Free space wavelength (nm)")

fig.tight_layout()

fig.savefig("./example_figures/psi_delta.png")

plt.show()
