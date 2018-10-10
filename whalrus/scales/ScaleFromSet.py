from whalrus.scales.ScaleFromList import ScaleFromList
from whalrus.utils.Utils import set_to_str


class ScaleFromSet(ScaleFromList):
    # noinspection PyUnresolvedReferences
    """
    Scale derived from a set.

    :param levels: a set of comparable objects. It is recommended that they are also hashable.

    >>> scale = ScaleFromSet({-1, 0, 2})
    >>> scale
    ScaleFromSet(levels={-1, 0, 2})
    >>> scale.lt(0, 2)
    True

    >>> class Appreciation:
    ...     VALUES = {'Excellent': 2, 'Good': 1, 'Medium': 0}
    ...     def __init__(self, x):
    ...         self.x = x
    ...     def __repr__(self):
    ...         return 'Appreciation(%r)' % self.x
    ...     def __hash__(self):
    ...         return hash(self.x)
    ...     def __lt__(self, other):
    ...         return Appreciation.VALUES[self.x] < Appreciation.VALUES[other.x]
    >>> scale = ScaleFromSet({Appreciation('Excellent'), Appreciation('Good'), Appreciation('Medium')})
    >>> scale
    ScaleFromSet(levels={Appreciation('Medium'), Appreciation('Good'), Appreciation('Excellent')})
    >>> scale.lt(Appreciation('Medium'), Appreciation('Good'))
    True
    >>> scale.low
    Appreciation('Medium')
    >>> scale.high
    Appreciation('Excellent')
    """

    def __init__(self, levels: set):
        super().__init__(sorted(levels))

    # noinspection PyMethodMayBeStatic
    def lt(self, one: object, another: object) -> bool:
        return one < another

    def __repr__(self):
        return 'ScaleFromSet(levels=%s)' % set_to_str(set(self.levels))
