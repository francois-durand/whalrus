from whalrus.rule.RuleScorePositional import RuleScorePositional
from whalrus.profile.Profile import Profile
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class RuleKApproval(RuleScorePositional):
    """
    K-Approval

    :param k: the number of approved candidates.

    The ``k`` top candidates in a ballot receive 1 point, and the other candidates receive 0 point.

    >>> RuleKApproval(['a > b > c', 'b > c > a'], k=2).scores_
    {'a': 1, 'b': 2, 'c': 1}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, tie_break: Priority = Priority.UNAMBIGUOUS,
                 default_converter: ConverterBallot = None):
        super().__init__(ballots=ballots, weights=weights, voters=voters, candidates=candidates, tie_break=tie_break,
                         default_converter=default_converter)
