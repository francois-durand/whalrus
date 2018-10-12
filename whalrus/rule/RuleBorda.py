from whalrus.rule.RuleScore import RuleScore
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.profile.Profile import Profile
from whalrus.priority.Priority import Priority
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.ballot.BallotOrder import BallotOrder


class RuleBorda(RuleScore):
    """
    The Borda rule.

    :param absent_give_points: if True, then candidates that are absent in ballot are considered as if they were
        at the bottom of the ballots.
    :param absent_receive_points: if True, then candidates that are absent from the ballot can receive points (for
        being considered as tied with other absent candidates).
    :param unordered_give_points: if True, then unordered candidates are considered as if they were at the bottom
        of the ballot (but above the absent candidates).
    :param unordered_receive_points: if True, then unordered candidates can receive points (for example, for
        being above the absent candidates, or tied with other unordered candidates).

    Cf. :class:`RulePlurality` and :class:`Rule` for the general syntax.

    >>> RuleBorda([
    ...     'a ~ b > c', 'b > c > a'
    ... ]).scores_ == {'a': 1.5, 'b': 3.5, 'c': 1}
    True

    In the example below, candidates a, b and c are "ordered", d and e are "unordered", and f and g are "absent" in the
    ballot, meaning that these candidates were not even available when the voter cast her ballot. The options allows
    for different ways to take these special cases into account.

    >>> profile = Profile([BallotOrder('a > b ~ c', candidates={'a', 'b', 'c', 'd', 'e'})])
    >>> candidates_election = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
    >>> RuleBorda(
    ...     profile, candidates=candidates_election
    ... ).scores_
    {'a': 6.0, 'b': 4.5, 'c': 4.5, 'd': 2.5, 'e': 2.5, 'f': 0.5, 'g': 0.5}
    >>> RuleBorda(
    ...     profile, candidates=candidates_election,
    ...     absent_receive_points=False
    ... ).scores_
    {'a': 6.0, 'b': 4.5, 'c': 4.5, 'd': 2.5, 'e': 2.5, 'f': 0.0, 'g': 0.0}
    >>> RuleBorda(
    ...     profile, candidates=candidates_election,
    ...     absent_receive_points=False, absent_give_points=False
    ... ).scores_
    {'a': 4.0, 'b': 2.5, 'c': 2.5, 'd': 0.5, 'e': 0.5, 'f': 0.0, 'g': 0.0}
    >>> RuleBorda(
    ...     profile, candidates=candidates_election,
    ...     absent_receive_points=False, absent_give_points=False,
    ...     unordered_receive_points=False
    ... ).scores_
    {'a': 4.0, 'b': 2.5, 'c': 2.5, 'd': 0.0, 'e': 0.0, 'f': 0.0, 'g': 0.0}
    >>> RuleBorda(
    ...     profile, candidates=candidates_election,
    ...     absent_receive_points=False, absent_give_points=False,
    ...     unordered_receive_points=False, unordered_give_points=False
    ... ).scores_
    {'a': 2.0, 'b': 0.5, 'c': 0.5, 'd': 0.0, 'e': 0.0, 'f': 0.0, 'g': 0.0}
    """

    def __init__(self, ballots=None, weights=None, voters=None, candidates=None, converter=None,
                 tie_break=Priority.UNAMBIGUOUS, default_converter=ConverterBallotToOrder(),
                 absent_give_points=True, absent_receive_points=True,
                 unordered_give_points=True, unordered_receive_points=True):
        self.absent_give_points = absent_give_points
        self.absent_receive_points = absent_receive_points
        self.unordered_give_points = unordered_give_points
        self.unordered_receive_points = unordered_receive_points
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter
        )

    @cached_property
    def scores_(self) -> NiceDict:
        scores_ = NiceDict({c: 0. for c in self.candidates_})
        for ballot, weight, _ in self.profile_converted_.items():
            if not isinstance(ballot, BallotOrder):
                raise ValueError
            points_from_lower_candidates = 0
            # Absent candidates
            if self.absent_give_points:
                absent = self.candidates_ - ballot.candidates
                n = len(absent)
                if self.absent_receive_points:
                    for c in absent:
                        scores_[c] += weight * (n - 1) / 2
                points_from_lower_candidates = n
            # Unordered candidates
            if self.unordered_give_points or self.unordered_receive_points:
                unordered = ballot.candidates_not_in_b
                n = len(unordered)
                if self.unordered_receive_points:
                    if self.unordered_give_points:
                        points_temp = points_from_lower_candidates + (n - 1) / 2
                    else:
                        points_temp = points_from_lower_candidates
                    for c in unordered:
                        scores_[c] += weight * points_temp
                if self.unordered_give_points:
                    points_from_lower_candidates += n
            # Ordered candidates
            for indifference_class in ballot.as_weak_order[::-1]:
                n = len(indifference_class)
                points_temp = points_from_lower_candidates + (n - 1) / 2
                for c in indifference_class:
                    scores_[c] += weight * points_temp
                points_from_lower_candidates += n
        return scores_
