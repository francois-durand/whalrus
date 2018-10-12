from whalrus.utils.Utils import cached_property
from whalrus.rule.Rule import Rule
from whalrus.rule.RulePlurality import RulePlurality
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.priority.Priority import Priority
from typing import Union


class RuleSequentialElimination(Rule):
    """
    A rule by sequential elimination of the trailer candidate (such as IRV, Coombs, Baldwin...)

    :param base_rule: the rule used at each round to determine the trailing candidate.

    >>> irv = RuleSequentialElimination(base_rule=RulePlurality())
    >>> irv(['a > b > c', 'b > a > c', 'c > a > b'],
    ...     weights=[2, 3, 4]).winner_
    'b'
    """

    def __init__(self, ballots: Union[list, Profile]=None, weights: list=None, voters: list=None,
                 candidates: set=None, converter: ConverterBallot=None,
                 tie_break: Priority=Priority.UNAMBIGUOUS, default_converter: ConverterBallot=ConverterBallotGeneral(),
                 base_rule: Rule=None):
        self.base_rule = base_rule
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter
        )

    @cached_property
    def order_(self) -> list:
        candidates = self.candidates_.copy()
        result = []
        while candidates:
            trailer = self.base_rule(self.profile_converted_, candidates=candidates).trailer_
            result.insert(0, {trailer})
            candidates.remove(trailer)
        return result
