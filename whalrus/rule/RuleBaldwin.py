from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.priority.Priority import Priority
from whalrus.rule.Rule import Rule
from whalrus.rule.RuleIteratedElimination import RuleIteratedElimination
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.elimination.Elimination import Elimination
from whalrus.elimination.EliminationLast import EliminationLast
from typing import Union


class RuleBaldwin(RuleIteratedElimination):
    """
    Baldwin's rule.

    At each round, the candidate with the worst Borda score is eliminated.

    >>> rule = RuleBaldwin(['a > b > c', 'a > b ~ c'])
    >>> rule.eliminations_[0].rule_.scores_
    {'a': 4.0, 'b': 1.5, 'c': 0.5}
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
            elimination = EliminationLast(k=1)
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter,
            base_rule=base_rule, elimination=elimination, propagate_tie_break=propagate_tie_break
        )
