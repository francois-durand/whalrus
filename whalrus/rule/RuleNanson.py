from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.priority.Priority import Priority
from whalrus.rule.Rule import Rule
from whalrus.rule.RuleIteratedElimination import RuleIteratedElimination
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.elimination.Elimination import Elimination
from whalrus.elimination.EliminationBelowAverage import EliminationBelowAverage
from typing import Union


class RuleNanson(RuleIteratedElimination):
    """
    Nanson's rule.

    At each round, all candidates whose Borda score is lower than the average Borda score are eliminated.

    >>> rule = RuleNanson(['a > b > c > d', 'a > b > d > c'])
    >>> rule.eliminations_[0].rule_.scores_
    {'a': 6.0, 'b': 4.0, 'c': 1.0, 'd': 1.0}
    >>> rule.eliminations_[1].rule_.scores_
    {'a': 2.0, 'b': 0.0}
    >>> rule.eliminations_[2].rule_.scores_
    {'a': 0.0}
    >>> rule.winner_
    'a'
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, default_converter: ConverterBallot = None,
                 base_rule: Rule = None, elimination: Elimination = None, propagate_tie_break=True):
        if base_rule is None:
            base_rule = RuleBorda()
        if elimination is None:
            elimination = EliminationBelowAverage()
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter,
            base_rule=base_rule, elimination=elimination, propagate_tie_break=propagate_tie_break
        )
