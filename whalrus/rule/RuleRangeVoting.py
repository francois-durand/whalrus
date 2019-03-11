from whalrus.scale.ScaleRange import ScaleRange
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.converter_ballot.ConverterBallotToGrades import ConverterBallotToGrades
from whalrus.priority.Priority import Priority
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.profile.Profile import Profile
from typing import Union
import numbers


class RuleRangeVoting(RuleScoreNum):
    """
    Range voting.

    :param default_converter: the default is :class:`ConverterBallotToGrades`.
    :param grade_ungraded: the default grade when a ballot does not grade a candidate (partial or total abstention).
        If None (default), then the average grade is computed only over non-abstainers (cf. examples below).
    :param grade_absent: the default grade when a voter did not even see the candidate (i.e. it is not in its
        attribute ``candidates``). If None (default), then the average grade is computed only over non-abstainers (cf.
        examples below).
    :param default_average: the final score that a candidate has when it receives absolutely no grade whatsoever.
        This avoids a division by 0 when computing the average grade.

    Cf. :class:`RulePlurality` and :class:`Rule` for the general syntax.

    >>> RuleRangeVoting([{'a': 1., 'b': .8, 'c': .2}, {'a': 0., 'b': .6, 'c': 1.}]).scores_
    {'a': 0.5, 'b': 0.7, 'c': 0.6}
    >>> RuleRangeVoting([{'a': 10, 'b': 8, 'c': 2}, {'a': 0, 'b': 6, 'c': 10}]).scores_
    {'a': 5.0, 'b': 7.0, 'c': 6.0}

    With ballot conversion:

    >>> RuleRangeVoting(['a > b > c', 'c > a > b']).scores_
    {'a': 0.75, 'b': 0.25, 'c': 0.5}
    >>> RuleRangeVoting(['a > b > c', 'c > a > b'], default_converter=ConverterBallotToGrades(
    ...     scale=ScaleRange(0, 10))).scores_
    {'a': 7.5, 'b': 2.5, 'c': 5.0}

    About the options:

    >>> b1 = BallotLevels({'a': 8, 'b': 10}, candidates={'a', 'b'})  # 'c' is absent
    >>> b2 = BallotLevels({'a': 6, 'c': 10}, candidates={'a', 'b', 'c'})  # 'b' is present but ungraded
    >>> RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'}).scores_
    {'a': 7.0, 'b': 10.0, 'c': 10.0, 'd': 0.0}
    >>> RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'}, default_average=5.).scores_
    {'a': 7.0, 'b': 10.0, 'c': 10.0, 'd': 5.0}
    >>> RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'}, grade_ungraded=0.).scores_
    {'a': 7.0, 'b': 5.0, 'c': 10.0, 'd': 0.0}
    >>> RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'}, grade_ungraded=0., grade_absent=0.).scores_
    {'a': 7.0, 'b': 5.0, 'c': 5.0, 'd': 0.0}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, tie_break: Priority = Priority.UNAMBIGUOUS,
                 default_converter: ConverterBallot = None):
        if default_converter is None:
            default_converter = ConverterBallotToGrades()
        self.grade_ungraded = grade_ungraded
        self.grade_absent = grade_absent
        self.default_average = default_average
        super().__init__(ballots=ballots, weights=weights, voters=voters, candidates=candidates, tie_break=tie_break,
                         default_converter=default_converter)

    @cached_property
    def scores_(self) -> NiceDict:
        scores_ = NiceDict({c: 0. for c in self.candidates_})
        total_weights = NiceDict({c: 0. for c in self.candidates_})
        for ballot, weight, _ in self.profile_converted_.items():
            if self.grade_absent is not None:
                for c in (self.candidates_ - ballot.candidates):
                    scores_[c] += self.grade_absent
                    total_weights[c] += weight
            if self.grade_ungraded is not None:
                for c in ballot.candidates_not_in_b:
                    scores_[c] += self.grade_ungraded
                    total_weights[c] += weight
            for c, grade in ballot.items():
                scores_[c] += grade
                total_weights[c] += weight
        return NiceDict({c: v / total_weights[c] if total_weights[c] > 0 else self.default_average
                         for c, v in scores_.items()})
