from whalrus.utils.Utils import cached_property
from whalrus.rule.Rule import Rule
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.rule.RulePlurality import RulePlurality
from whalrus.rule.RuleSequentialElimination import RuleSequentialElimination
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.priority.Priority import Priority
from whalrus.elimination.Elimination import Elimination
from whalrus.elimination.EliminationLast import EliminationLast
from typing import Union


class RuleTwoRound(RuleSequentialElimination):
    # noinspection PyUnresolvedReferences
    """
    The two-round system.

    :param rule1: the first rule. Default: :class:`Plurality`.
    :param rule2: the second rule. Default: :class:`Plurality`.
    :param elimination: the elimination algorithm used during the first round. Default: ``EliminationLast(k=-2)``,
        which only keeps the 2 best candidates.

    With its default settings, this class implements the classic two-round system, using plurality at both rounds:

    >>> rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'], weights=[2, 2, 1])
    >>> rule.first_round_.rule_.brute_scores_
    {'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 0}
    >>> rule.second_round_.brute_scores_
    {'a': 3, 'b': 2}

    Using the options, more exotic two-round systems can be defined, such as changing the rule of a round:

    >>> rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'], weights=[2, 2, 1],
    ...                     rule1=RuleBorda())
    >>> rule.first_round_.rule_.brute_scores_
    {'a': 17.0, 'b': 16.0, 'c': 12.0, 'd': 5.0, 'e': 0.0}
    >>> rule.second_round_.brute_scores_
    {'a': 3, 'b': 2}

    ... or changing the elimination criterion:

    >>> rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'], weights=[2, 2, 1],
    ...                     elimination=EliminationLast(k=-3))
    >>> rule.first_round_.rule_.brute_scores_
    {'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 0}
    >>> rule.second_round_.brute_scores_
    {'a': 2, 'b': 2, 'c': 1}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 rule1: Rule = None, rule2: Rule = None, elimination: Elimination = None,
                 propagate_tie_break=True):
        if rule1 is None:
            rule1 = RulePlurality()
        if rule2 is None:
            rule2 = RulePlurality()
        if elimination is None:
            elimination = EliminationLast(k=-2)
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter,
            rules=[rule1, rule2], eliminations=[elimination], propagate_tie_break=propagate_tie_break
        )

    @cached_property
    def first_round_(self) -> Elimination:
        """
        The first round.

        :return: an :class:`Elimination` object, the first round. This is just a shortcut for
            ``self.elimination_rounds_[0]``.
        """
        return self.elimination_rounds_[0]

    @cached_property
    def second_round_(self) -> Rule:
        """
        The second round.

        :return: a :class:`Rule` object, the second round. This is just an alternative name for ``self.final_round_``.
        """
        return self.final_round_
