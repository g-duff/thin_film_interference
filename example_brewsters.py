import numpy as np
import matplotlib.pyplot as plt
import src.ellipsometer as el
import src.fresnel as fr


coverRefractiveIndex = 1.0
substrateRefractiveIndex = 1.45
incidentAngle = np.arange(0, 90)

incidentAngleInRadians = np.deg2rad(incidentAngle)

transmissionAngle = el.calculateTransmissionAngle(
    coverRefractiveIndex, substrateRefractiveIndex, incidentAngleInRadians
)
senkrechtReflection = fr.Senkrecht.reflection(
    incidentAngleInRadians,
    transmissionAngle,
)
parallelReflection = fr.Parallel.reflection(
    incidentAngleInRadians,
    transmissionAngle,
)

fig, ax = plt.subplots()

ax.plot(incidentAngle, np.abs(senkrechtReflection) ** 2, "C0", label="S polarisation")
ax.plot(incidentAngle, np.abs(parallelReflection) ** 2, "C3", label="P polarisation")

ax.set_xlabel("Angle of incidence (degrees)")
ax.set_ylabel("Reflectance")
ax.legend()

fig.savefig("./example_figures/brewsters.png")

plt.show()
