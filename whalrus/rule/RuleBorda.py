from whalrus.rule.RuleScoreNumAverage import RuleScoreNumAverage
from whalrus.scorer.Scorer import Scorer
from whalrus.scorer.ScorerBorda import ScorerBorda
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.profile.Profile import Profile
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union
from numbers import Number


class RuleBorda(RuleScoreNumAverage):
    """
    The Borda rule.

    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param scorer: the default is :class:`ScorerBorda`.

    Cf. :class:`RulePlurality` and :class:`Rule` for the general syntax.

    >>> rule = RuleBorda(['a ~ b > c', 'b > c > a'])
    >>> rule.brute_scores_
    {'a': 1.5, 'b': 3.5, 'c': 1.0}
    >>> rule.scores_
    {'a': 0.75, 'b': 1.75, 'c': 0.5}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 scorer: Scorer = None, default_average: Number = None):
        if converter is None:
            converter = ConverterBallotToOrder()
        if scorer is None:
            scorer = ScorerBorda()
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter,
            scorer=scorer, default_average=default_average
        )
