from whalrus.scales.Scale import Scale


class ScaleInterval(Scale):
    """
    A scale given by an interval of floats.

    :param low: lowest float.
    :param high: highest float.

    >>> ScaleInterval(low=0., high=10.)
    ScaleInterval(low=0.0, high=10.0)
    """

    def __init__(self, low: float = 0., high: float = 1.):
        self.low = low
        self.high = high

    def __repr__(self):
        return 'ScaleInterval(low=%s, high=%s)' % (self.low, self.high)
