from whalrus.rule.RuleScore import RuleScore
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.profile.Profile import Profile
from whalrus.priority.Priority import Priority
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class RuleScorePositional(RuleScore):
    """
    A positional scoring rule.

    :param default_converter: the default is :class:`ConverterBallotToOrder`.
    :param points_scheme: the list of points to be attributed to the (first) candidates of a ballot.

    The ballots must be strict orders (or converted to strict orders by the chosen ``converter``). The top candidate
    in a ballot receives ``points_scheme[0]`` points, the second one receives ``points_scheme[1]` points, etc.

    >>> RuleScorePositional(['a > b > c', 'b > c > a'], points_scheme=[3, 2, 1]).scores_
    {'a': 4, 'b': 5, 'c': 3}

    The points scheme does not need to have the same length as the ballots:

    >>> RuleScorePositional(['a > b > c', 'b > c > a'], points_scheme=[3, 2, 1, .5]).scores_
    {'a': 4, 'b': 5, 'c': 3}
    >>> RuleScorePositional(['a > b > c', 'b > c > a'], points_scheme=[3, 2]).scores_
    {'a': 3, 'b': 5, 'c': 2}

    A typical usage of this is k-Approval voting:

    >>> RuleScorePositional(['a > b > c', 'b > c > a'], points_scheme=[1, 1]).scores_
    {'a': 1, 'b': 2, 'c': 1}

    Note that the :class:`RuleKApproval` constitutes a convenient shortcut for the above voting rule.
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, default_converter: ConverterBallot = None,
                 points_scheme: list = None):
        if default_converter is None:
            default_converter = ConverterBallotToOrder()
        # if points_scheme is None:
        #     points_scheme = [1]
        self.points_scheme = points_scheme
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter
        )

    @cached_property
    def scores_(self) -> NiceDict:
        scores_ = NiceDict({c: 0 for c in self.candidates_})
        for ballot, weight, _ in self.profile_converted_.items():
            for i, c in enumerate(ballot):
                if i < len(self.points_scheme):
                    scores_[c] += self.points_scheme[i]
                else:
                    break
        return scores_
