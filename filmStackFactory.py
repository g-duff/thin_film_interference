import functools


def linkLayers(filmRefractiveIndices, filmThicknesses):
    substrateRefractiveIndex = filmRefractiveIndices.pop()

    return functools.reduce(
        lambda previous, current: linkedLayers(
            current[0], thickness=current[1], nextLayer=previous
        ),
        zip(filmRefractiveIndices[::-1], filmThicknesses[::-1]),
        linkedLayers(substrateRefractiveIndex),
    )


class linkedLayers:
    def __init__(self, refractiveIndex, thickness=None, nextLayer=None):
        self.refractiveIndex = refractiveIndex
        self.thickness = thickness
        self.nextLayer = nextLayer

    def hasNextLayer(self):
        return self.nextLayer != None
