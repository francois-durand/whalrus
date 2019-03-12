from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.scale.Scale import Scale
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.scorer.Scorer import Scorer
from numbers import Number
from typing import Union


class ScorerPositional(Scorer):
    """
    A positional scorer for strict order ballots.

    :param points_scheme: the list of points to be attributed to the (first) candidates of a ballot.
    :param points_fill: points for ordered candidates that have a rank beyond the ``points_scheme``.
    :param points_unordered: points for the unordered candidates.
    :param points_absent: points for the absent candidates.

    The top candidate in the ballot receives ``points_scheme[0]`` points, the second one receives ``points_scheme[1]`
    points, etc.

    >>> ScorerPositional(ballot=BallotOrder('a > b > c'), points_scheme=[10, 5, 3]).scores_
    {'a': 10, 'b': 5, 'c': 3}

    The points scheme does not need to have the same length as the ballot:

    >>> ScorerPositional(ballot=BallotOrder('a > b > c'), points_scheme=[3, 2, 1, .5]).scores_
    {'a': 3, 'b': 2, 'c': 1}
    >>> ScorerPositional(ballot=BallotOrder('a > b > c'), points_scheme=[3, 2]).scores_
    {'a': 3, 'b': 2, 'c': 0}

    A typical usage of this is k-Approval voting:

    >>> ScorerPositional(ballot=BallotOrder('a > b > c > d > e'), points_scheme=[1, 1]).scores_
    {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 0}

    In the example below, candidates ``a``, ``b`` and ``c`` are `ordered', ``d`` is `unordered', and ``e`` is `absent'
    in the ballot, meaning that ``e`` were not even available when the voter cast her ballot. The options of the
    scorer provide different ways to take these special cases into account.

    >>> ballot=BallotOrder('a > b > c', candidates={'a', 'b', 'c', 'd'})
    >>> candidates_election = {'a', 'b', 'c', 'd', 'e'}
    >>> ScorerPositional(ballot, candidates=candidates_election, points_scheme=[3, 2]).scores_
    {'a': 3, 'b': 2, 'c': 0, 'd': 0}
    >>> ScorerPositional(ballot, candidates=candidates_election, points_scheme=[3, 2],
    ...     points_fill=.3, points_unordered=.2, points_absent=.1).scores_
    {'a': 3, 'b': 2, 'c': 0.3, 'd': 0.2, 'e': 0.1}
    >>> ScorerPositional(ballot, candidates=candidates_election, points_scheme=[3, 2],
    ...     points_fill=None, points_unordered=None, points_absent=None).scores_
    {'a': 3, 'b': 2}
    """

    def __init__(self, ballot: BallotOrder = None, voter: object = None, candidates: set = None,
                 scale: Scale = None,
                 points_scheme: list = None, points_fill: Union[Number, None] = 0,
                 points_unordered: Union[Number, None] = 0, points_absent: Union[Number, None] = None):
        self.points_scheme = points_scheme
        self.points_fill = points_fill
        self.points_unordered = points_unordered
        self.points_absent = points_absent
        super().__init__(ballot=ballot, voter=voter, candidates=candidates, scale=scale)

    @cached_property
    def scores_(self) -> NiceDict:
        scores = NiceDict()
        l_points_scheme = len(self.points_scheme)
        for i, c in enumerate(self.ballot_):
            if i < l_points_scheme:
                scores[c] = self.points_scheme[i]
            else:
                if self.points_fill is None:
                    break
                scores[c] = self.points_fill
        if self.points_unordered is not None:
            scores.update({c: self.points_unordered for c in self.ballot_.candidates_not_in_b})
        if self.points_absent is not None:
            scores.update({c: self.points_absent for c in self.candidates_ - self.ballot_.candidates})
        return scores
