from whalrus.scales.Scale import Scale


class ScaleRange(Scale):
    """
    A scale of consecutive integers.

    :param low: lowest integer.
    :param high: highest integer.

    Remark: for a scale of non-consecutive integers, such as {-1, 0, 2}, use the class ScaleFromSet.

    >>> ScaleRange(low=0, high=5)
    ScaleRange(low=0, high=5)
    """

    def __init__(self, low: int, high: int):
        self.low = low
        self.high = high

    def __repr__(self):
        return 'ScaleRange(low=%s, high=%s)' % (self.low, self.high)
