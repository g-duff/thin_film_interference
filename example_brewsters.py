import numpy as np
import matplotlib.pyplot as plt
import ellipsometerUtils as el

# Input

coverRefractiveIndex = 1.0
substrateRefractiveIndex = 1.45

incidentAngle = np.arange(0, 90)*el.degrees

# Calculation
transmissionAngle = el.calculateTransmissionAngle(coverRefractiveIndex, substrateRefractiveIndex, incidentAngle)

senkrechtReflection = el.calculateSenkrechtReflection(coverRefractiveIndex, substrateRefractiveIndex, incidentAngle, transmissionAngle)
parallelReflection = el.calculateParallelReflection(coverRefractiveIndex, substrateRefractiveIndex, incidentAngle, transmissionAngle)

# Graphical output

fig, ax = plt.subplots()

ax.plot(incidentAngle, np.abs(senkrechtReflection)**2, 'C0--', label="S polarisation")
ax.plot(incidentAngle, np.abs(parallelReflection)**2, 'C3--', label="P polarisation")

ax.set_xlabel('Angle of incidence (degrees)')
ax.set_ylabel('Reflectance')
ax.legend()

fig.savefig('./example_figures/brewsters.png')

plt.show()
