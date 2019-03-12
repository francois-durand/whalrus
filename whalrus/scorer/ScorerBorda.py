from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.scale.Scale import Scale
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.scorer.Scorer import Scorer
from typing import Union


class ScorerBorda(Scorer):
    """
    A Borda scorer for :class:`BallotOrder`.

    :param absent_give_points: whether absent candidates give points to the other candidates.
    :param absent_receive_points: whether absent candidates receives points. Remark: 0. means that the absent
        candidate receives 0 (which will be counted in its average Borda score, median Borda score, etc); in contrast,
        None means that the absent candidate receives no score (hence this voter will be exclued from the computation
        of its average Borda score, median Borda score, etc).
    :param unordered_give_points: whether unordered candidates give points to the ordered candidates, i.e. they are
        considered as being in a lower position in the ranking.
    :param unordered_receive_points: whether unordered candidates receive points. Like for ``absent_receive_points``,
        None is possible.

    Typical usage:

    >>> ScorerBorda(ballot=BallotOrder('a > b > c'), voter='Alice', candidates={'a', 'b', 'c'}).scores_
    {'a': 2.0, 'b': 1.0, 'c': 0.0}

    In the example below, candidates ``a``, ``b`` and ``c`` are `ordered', ``d`` and ``e`` are `unordered', and ``f``
    and ``g`` are `absent' in the ballot, meaning that these candidates were not even available when the voter cast
    her ballot. The options allows for different ways to take these special cases into account.

    >>> ballot = BallotOrder('a > b ~ c', candidates={'a', 'b', 'c', 'd', 'e'})
    >>> candidates_election = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    >>> ScorerBorda(ballot, candidates=candidates_election).scores_
    {'a': 6.0, 'b': 4.5, 'c': 4.5, 'd': 2.5, 'e': 2.5, 'f': 0.5, 'g': 0.5}
    >>> ScorerBorda(ballot, candidates=candidates_election,
    ...             absent_receive_points=False).scores_
    {'a': 6.0, 'b': 4.5, 'c': 4.5, 'd': 2.5, 'e': 2.5, 'f': 0.0, 'g': 0.0}
    >>> ScorerBorda(ballot, candidates=candidates_election,
    ...             absent_receive_points=False, absent_give_points=False).scores_
    {'a': 4.0, 'b': 2.5, 'c': 2.5, 'd': 0.5, 'e': 0.5, 'f': 0.0, 'g': 0.0}
    >>> ScorerBorda(ballot, candidates=candidates_election,
    ...             absent_receive_points=False, absent_give_points=False,
    ...             unordered_receive_points=False).scores_
    {'a': 4.0, 'b': 2.5, 'c': 2.5, 'd': 0.0, 'e': 0.0, 'f': 0.0, 'g': 0.0}
    >>> ScorerBorda(ballot, candidates=candidates_election,
    ...             absent_receive_points=False, absent_give_points=False,
    ...             unordered_receive_points=False, unordered_give_points=False).scores_
    {'a': 2.0, 'b': 0.5, 'c': 0.5, 'd': 0.0, 'e': 0.0, 'f': 0.0, 'g': 0.0}

    Usage of None in the arguments:

    >>> ScorerBorda(ballot, candidates=candidates_election,
    ...             absent_receive_points=None, unordered_receive_points=None).scores_
    {'a': 6.0, 'b': 4.5, 'c': 4.5}
    """

    def __init__(self, ballot: BallotOrder = None, voter: object = None, candidates: set = None,
                 scale: Scale = None,
                 absent_give_points: bool = True, absent_receive_points: Union[bool, None] = True,
                 unordered_give_points: bool = True, unordered_receive_points: Union[bool, None] = True):
        self.absent_give_points = absent_give_points
        self.absent_receive_points = absent_receive_points
        self.unordered_give_points = unordered_give_points
        self.unordered_receive_points = unordered_receive_points
        super().__init__(ballot=ballot, voter=voter, candidates=candidates, scale=scale)

    @cached_property
    def scores_(self) -> NiceDict:
        scores = NiceDict()
        points_from_lower_candidates = 0.
        # Absent candidates
        if self.absent_give_points or self.absent_receive_points is not None:
            absent = self.candidates_ - self.ballot_.candidates
            n_absent = len(absent)
            if self.absent_receive_points is False:
                scores.update({c: 0. for c in absent})
            if self.absent_receive_points is True:
                points_temp = (n_absent - 1) / 2 if self.absent_give_points else 0.
                scores.update({c: points_temp for c in absent})
            if self.absent_give_points:
                points_from_lower_candidates += n_absent
        # Unordered candidates
        if self.unordered_give_points or self.unordered_receive_points is not None:
            unordered = self.ballot_.candidates_not_in_b
            n_unordered = len(unordered)
            if self.unordered_receive_points is False:
                scores.update({c: 0. for c in unordered})
            if self.unordered_receive_points is True:
                points_temp = points_from_lower_candidates
                if self.unordered_give_points:
                    points_temp += (n_unordered - 1) / 2
                scores.update({c: points_temp for c in unordered})
            if self.unordered_give_points:
                points_from_lower_candidates += n_unordered
        # Ordered candidates
        for indifference_class in self.ballot_.as_weak_order[::-1]:
            n_indifference = len(indifference_class)
            points_temp = points_from_lower_candidates + (n_indifference - 1) / 2
            scores.update({c: points_temp for c in indifference_class})
            points_from_lower_candidates += n_indifference
        return scores
