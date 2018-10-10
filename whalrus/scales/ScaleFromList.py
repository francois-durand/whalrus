from whalrus.scales.Scale import Scale


class ScaleFromList(Scale):
    """
    Scale derived from a list.

    :param levels: list of levels, from the worst to the best.

    >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
    >>> scale
    ScaleFromList(levels=['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
    >>> scale.lt('Medium', 'Excellent')
    True
    >>> scale.gt('Medium', 'Excellent')
    False
    >>> scale.low
    'Bad'
    >>> scale.high
    'Excellent'
    """

    def __init__(self, levels: list):
        self.levels = list(levels)
        self._as_dict = {evaluation: rank for rank, evaluation in enumerate(levels)}

    def lt(self, one: object, another: object) -> bool:
        return self._as_dict[one] < self._as_dict[another]

    @property
    def low(self) -> object:
        """
        Lowest level of the scale.

        :return: the lowest level.
        """
        return self.levels[0]

    @property
    def high(self) -> object:
        """
        Highest level of the scale.

        :return: the highest level.
        """
        return self.levels[-1]

    def __repr__(self):
        return 'ScaleFromList(levels=%s)' % self.levels
