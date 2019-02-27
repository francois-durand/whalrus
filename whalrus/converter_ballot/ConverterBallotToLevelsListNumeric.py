from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotToLevelsInterval import ConverterBallotToLevelsInterval
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.scale.ScaleInterval import ScaleInterval
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.scale.ScaleFromSet import ScaleFromSet
from whalrus.scale.ScaleRange import ScaleRange
from whalrus.utils.Utils import take_closest


class ConverterBallotToLevelsListNumeric(ConverterBallot):
    """
    Default converter to a ``level / numeric'' ballot (suitable for Range Voting).

    :param scale: the scale.
    :param borda_unordered_give_points: when converting a :class:`BallotOrder`, we use Borda scores (normalized
        to the interval ``[low, high]`` and rounded). This parameter decides whether unordered candidates of the ballot
        give points to ordered candidates. Cf. meth:`BallotOrder.borda`.

    This is a default converter to a ballot using a list of numeric levels. It tries to infer the type of input and
    converts it to a :class:`BallotLevels`, where the scale is of class :class:`ScaleFromList`. Its functions
    essentially the same as class:`ConverterBallotToLevelsInterval`, but it then maps to the levels.

    Typical usages:

    >>> converter = ConverterBallotToLevelsListNumeric(scale=ScaleFromList([-1, 0, 3, 4]))
    >>> converter(BallotLevels({'a': 1., 'b': 0.2}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(-1., 1.))).as_dict
    {'a': 4, 'b': 3}
    >>> converter(BallotLevels({'a': 5, 'b': 4}, candidates={'a', 'b', 'c'}, scale=ScaleRange(0, 5))).as_dict
    {'a': 4, 'b': 3}
    >>> converter(BallotLevels({'a': 4, 'b': 0}, candidates={'a', 'b', 'c'}, scale=ScaleFromSet({-1, 0, 4}))).as_dict
    {'a': 4, 'b': 0}
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 4, 'b': -1, 'c': -1}
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 4, 'b': -1, 'c': -1}
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': -1, 'b': 4, 'c': 4}
    >>> converter('a > b > c > d').as_dict
    {'a': 4, 'b': 3, 'c': 0, 'd': -1}
    """

    def __init__(self, scale, borda_unordered_give_points: bool=True):
        self.scale = scale
        self.borda_unordered_give_points = borda_unordered_give_points

    def __call__(self, x: object, candidates: set =None) -> BallotLevels:
        x = ConverterBallotToLevelsInterval(
            scale=ScaleInterval(low=self.scale.low, high=self.scale.high),
            borda_unordered_give_points=self.borda_unordered_give_points
        )(x, candidates=None)
        return BallotLevels({c: take_closest(self.scale.levels, v) for c, v in x.items()},
                            candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
