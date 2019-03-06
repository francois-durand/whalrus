from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.rule.Rule import Rule
from whalrus.rule.RuleIteratedElimination import RuleIteratedElimination
from whalrus.rule.RulePlurality import RulePlurality
from whalrus.elimination.Elimination import Elimination
from whalrus.elimination.EliminationLast import EliminationLast
from whalrus.priority.Priority import Priority
from typing import Union


class RuleIRV(RuleIteratedElimination):
    """
    Instant-Runoff Voting, also known as Alternative vote, Single Transferable Vote, etc.

    At each round, the candidate with the worst Plurality score is eliminated.

    >>> rule = RuleIRV(['a > b > c', 'b > a > c', 'c > a > b'], weights=[2, 3, 4])
    >>> rule.eliminations_[0].rule_.scores_
    {'a': 2, 'b': 3, 'c': 4}
    >>> rule.eliminations_[1].rule_.scores_
    {'b': 5, 'c': 4}
    >>> rule.eliminations_[2].rule_.scores_
    {'b': 9}
    >>> rule.winner_
    'b'

    Using the tie-break:

    >>> rule = RuleIRV(['a > c > b', 'b > a > c', 'c > a > b'], weights=[1, 2, 1], tie_break=Priority.ASCENDING)
    >>> rule.eliminations_[0].rule_.scores_
    {'a': 1, 'b': 2, 'c': 1}
    >>> rule.eliminations_[1].rule_.scores_
    {'a': 2, 'b': 2}
    >>> rule.eliminations_[2].rule_.scores_
    {'a': 4}
    >>> rule.winner_
    'a'
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, default_converter: ConverterBallot = None,
                 base_rule: Rule = None, elimination: Elimination = None):
        if base_rule is None:
            base_rule = RulePlurality()
        if elimination is None:
            elimination = EliminationLast(k=1)
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter,
            base_rule=base_rule, elimination=elimination
        )
