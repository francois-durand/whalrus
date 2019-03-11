from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixWeightedMajority import MatrixWeightedMajority
from typing import Union


class RuleMaximin(RuleScoreNum):
    """
    Maximin rule.

    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_weighted_majority: a :class:`Matrix`. Default: :class:`MatrixWeightedMajority`.

    The score of a candidate is the minimal non-diagonal coefficient on its raw of the matrix.

    >>> rule = RuleMaximin(ballots=['a > b > c', 'b > c > a', 'c > a > b'], weights=[4, 3, 3])
    >>> rule.matrix_weighted_majority_.as_array_
    array([[0. , 0.7, 0.4],
           [0.3, 0. , 0.7],
           [0.6, 0.3, 0. ]])
    >>> rule.scores_
    {'a': 0.4, 'b': 0.3, 'c': 0.3}
    >>> rule.winner_
    'a'
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 matrix_weighted_majority: Matrix = None):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_weighted_majority is None:
            matrix_weighted_majority = MatrixWeightedMajority()
        self.matrix_weighted_majority = matrix_weighted_majority
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter
        )

    @cached_property
    def matrix_weighted_majority_(self):
        """
        The weighted majority matrix.

        :return: the weighted majority matrix (once computed with the given profile).
        """
        return self.matrix_weighted_majority(self.profile_converted_)

    @cached_property
    def scores_(self) -> NiceDict:
        matrix = self.matrix_weighted_majority_
        return NiceDict({c: min({v for (i, j), v in matrix.as_dict_.items() if i == c and j != c})
                         for c in matrix.candidates_})
