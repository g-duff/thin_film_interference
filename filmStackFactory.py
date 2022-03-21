import functools


def linkRefractiveIndices(
    filmRefractiveIndices,
):
    substrateRefractiveIndex = filmRefractiveIndices.pop()
    return functools.reduce(
        lambda previous, current: linkedList(current, previous),
        filmRefractiveIndices[::-1],
        linkedList(substrateRefractiveIndex),
    )


def linkThicknesses(filmThicknesses):
    bottomFilm = filmThicknesses.pop()
    return functools.reduce(
        lambda previous, current: linkedList(current, previous),
        filmThicknesses[::-1],
        linkedList(bottomFilm),
    )


class linkedList:
    def __init__(self, thisValue, nextValue=None):
        self.thisValue = thisValue
        self.nextValue = nextValue
