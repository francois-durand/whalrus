from whalrus.scale.ScaleRange import ScaleRange
from whalrus.rule.RuleRangeVoting import RuleRangeVoting
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotToGrades import ConverterBallotToGrades
from whalrus.priority.Priority import Priority
from whalrus.profile.Profile import Profile
from typing import Union
import numbers


class RuleApproval(RuleRangeVoting):
    """
    Approval voting.

    :param converter: the default is ``ConverterBallotToGrades(scale=ScaleRange(0, 1))``.

    Cf. :class:`RulePlurality` and :class:`Rule` for the general syntax.

    >>> RuleApproval([{'a': 1, 'b': 0, 'c': 0}, {'a': 1, 'b': 1, 'c': 0}]).scores_
    {'a': 1.0, 'b': 0.5, 'c': 0.0}

    With ballot conversion:

    >>> RuleApproval(['a > b > c > d', 'c > a > b > d']).scores_
    {'a': 1.0, 'b': 0.5, 'c': 0.5, 'd': 0.0}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 grade_ungraded: Union[numbers.Number, None] = None,
                 grade_absent: Union[numbers.Number, None] = None,
                 default_average: numbers.Number = 0.):
        if converter is None:
            converter = ConverterBallotToGrades(scale=ScaleRange(0, 1))
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter,
            grade_ungraded=grade_ungraded, grade_absent=grade_absent, default_average=default_average
        )
