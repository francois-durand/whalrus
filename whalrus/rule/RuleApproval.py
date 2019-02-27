from whalrus.scale.ScaleRange import ScaleRange
from whalrus.rule.RuleRangeVoting import RuleRangeVoting
from whalrus.converter_ballot.ConverterBallotToGrades import ConverterBallotToGrades
from whalrus.priority.Priority import Priority


class RuleApproval(RuleRangeVoting):
    """
    Approval voting.

    Cf. :class:`RulePlurality` and :class:`Rule` for the general syntax.

    >>> RuleApproval([{'a': 1, 'b': 0, 'c': 0}, {'a': 1, 'b': 1, 'c': 0}]).scores_
    {'a': 1.0, 'b': 0.5, 'c': 0.0}

    With ballot conversion:

    >>> RuleApproval(['a > b > c > d', 'c > a > b > d']).scores_
    {'a': 1.0, 'b': 0.5, 'c': 0.5, 'd': 0.0}
    """

    def __init__(self, ballots=None, weights=None, voters=None, candidates=None, converter=None,
                 tie_break=Priority.UNAMBIGUOUS, default_converter=ConverterBallotToGrades(scale=ScaleRange(0, 1)),
                 grade_ungraded=None, grade_absent=None, default_average=0.):
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter,
            grade_ungraded=grade_ungraded, grade_absent=grade_absent, default_average=default_average
        )
