from whalrus.rule.RuleScoreNumAverage import RuleScoreNumAverage
from whalrus.scorer.ScorerPositional import ScorerPositional
from whalrus.converter_ballot.ConverterBallotToStrictOrder import ConverterBallotToStrictOrder
from whalrus.profile.Profile import Profile
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class RuleScorePositional(RuleScoreNumAverage):
    """
    A positional scoring rule.

    :param converter: the default is :class:`ConverterBallotToStrictOrder`.
    :param points_scheme: the list of points to be attributed to the (first) candidates of a ballot.
        Cf. :class:`ScorerPositional`.

    >>> RuleScorePositional(['a > b > c', 'b > c > a'], points_scheme=[3, 2, 1]).brute_scores_
    {'a': 4, 'b': 5, 'c': 3}

    Since this voting rule needs strict orders, problems may occur as soon as there is indifference in the ballots. To
    avoid these issues, specify the ballot converter explicitly:

    >>> RuleScorePositional(['a > b ~ c', 'b > c > a'], points_scheme=[1, 1],
    ...     converter=ConverterBallotToStrictOrder(priority=Priority.ASCENDING)).brute_scores_
    {'a': 1, 'b': 2, 'c': 1}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 points_scheme: list = None):
        if converter is None:
            converter = ConverterBallotToStrictOrder()
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter,
            scorer=ScorerPositional(points_scheme=points_scheme), default_average=0
        )
