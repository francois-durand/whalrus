from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotToLevelsInterval import ConverterBallotToLevelsInterval
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.scale.ScaleInterval import ScaleInterval
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.scale.ScaleFromSet import ScaleFromSet
from whalrus.scale.ScaleRange import ScaleRange


class ConverterBallotToLevelsRange(ConverterBallot):
    """
    Default converter to an ``range'' ballot (suitable for Range Voting).

    :param low: the lowest grade in the scale.
    :param high: the highest grade in the scale.
    :param borda_unordered_give_points: when converting a :class:`BallotOrder`, we use Borda scores (normalized
        to the interval ``[low, high]`` and rounded). This parameter decides whether unordered candidates of the ballot
        give points to ordered candidates. Cf. meth:`BallotOrder.borda`.

    This is a default converter to a range ballot. It tries to infer the type of input and converts it to
    a :class:`BallotLevels`, where the scale is of class :class:`ScaleRange`. Its functions essentially the same
    as class:`ConverterBallotToLevelsInterval`, but it rounds the grades to the nearest integers.

    Typical usages:

    >>> converter = ConverterBallotToLevelsRange(low=0, high=10)
    >>> converter(BallotLevels({'a': 1., 'b': 0.4}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(-1., 1.)))
    BallotLevels({'a': 10, 'b': 7}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))
    >>> converter(BallotLevels({'a': 5, 'b': 4}, candidates={'a', 'b', 'c'}, scale=ScaleRange(0, 5)))
    BallotLevels({'a': 10, 'b': 8}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))
    >>> converter(BallotLevels({'a': 4, 'b': 0}, candidates={'a', 'b', 'c'}, scale=ScaleFromSet({-1, 0, 4})))
    BallotLevels({'a': 10, 'b': 2}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))
    >>> converter(BallotLevels({'a': 'Excellent', 'b': 'Very Good'}, candidates={'a', 'b', 'c'},
    ...                        scale=ScaleFromList(['Bad', 'Medium', 'Good', 'Very Good', 'Great', 'Excellent'])))
    BallotLevels({'a': 10, 'b': 6}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'}))
    BallotLevels({'a': 10, 'b': 0, 'c': 0}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))
    BallotLevels({'a': 10, 'b': 0, 'c': 0}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'}))
    BallotLevels({'a': 0, 'b': 10, 'c': 10}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))
    >>> converter('a > b > c')
    BallotLevels({'a': 10, 'b': 5, 'c': 0}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))

    Options for converting ordered ballots:

    >>> converter = ConverterBallotToLevelsRange(low=0, high=10, borda_unordered_give_points=False)
    >>> converter(BallotOrder('a > b > c', candidates={'a', 'b', 'c', 'd', 'e', 'f'}))  #doctest: +ELLIPSIS
    BallotLevels({'a': 10, 'b': 5, 'c': 0}, candidates={'a', ..., 'f'}, scale=ScaleRange(low=0, high=10))
    >>> converter = ConverterBallotToLevelsRange(low=0, high=10, borda_unordered_give_points=True)
    >>> converter(BallotOrder('a > b > c', candidates={'a', 'b', 'c', 'd', 'e', 'f'}))  #doctest: +ELLIPSIS
    BallotLevels({'a': 10, 'b': 8, 'c': 6}, candidates={'a', ..., 'f'}, scale=ScaleRange(low=0, high=10))
    """

    def __init__(self, low: int = 0, high: int = 1, borda_unordered_give_points: bool=True):
        self.low = low
        self.high = high
        self.scale = ScaleRange(low=low, high=high)
        self.borda_unordered_give_points = borda_unordered_give_points

    def __call__(self, x: object, candidates: set =None) -> BallotLevels:
        x = ConverterBallotToLevelsInterval(
            low=self.low, high=self.high, borda_unordered_give_points=self.borda_unordered_give_points
        )(x, candidates=None)
        return BallotLevels({c: round(v) for c, v in x.items()},
                            candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
