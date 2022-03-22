from numpy import cos


class OpticalPath:
    def __init__(self, refractiveIndex, thickness, rayAngle):
        self.refractiveIndex = refractiveIndex
        self.thickness = thickness
        self.rayAngle = rayAngle

    def accumulatePhase(self, freeSpaceWavenumber):
        opticalThickness = self.refractiveIndex * self.thickness
        opticalPathLength = 2 * opticalThickness * cos(self.rayAngle)
        return freeSpaceWavenumber * opticalPathLength
