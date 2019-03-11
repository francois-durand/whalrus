from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixMajority import MatrixMajority
from typing import Union


class RuleCopeland(RuleScoreNum):
    """
    Copeland's rule.

    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_majority: the majority matrix. Default: :class:`MatrixMajority`.

    The score of a candidate is the number of victories in the majority matrix. More exactly, it is the sum of
    the non-diagonal elements of its rows in the matrix.

    >>> rule = RuleCopeland(ballots=['a > b > c', 'b > a > c', 'c > a > b'])
    >>> rule.matrix_majority_.as_array_
    array([[0.5, 1. , 1. ],
           [0. , 0.5, 1. ],
           [0. , 0. , 0.5]])
    >>> rule.scores_
    {'a': 2.0, 'b': 1.0, 'c': 0.0}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 matrix_majority: Matrix = None):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_majority is None:
            matrix_majority = MatrixMajority()
        self.matrix_majority = matrix_majority
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter
        )

    @cached_property
    def matrix_majority_(self):
        """
        The majority matrix.

        :return: the majority matrix (once computed with the given profile).
        """
        return self.matrix_majority(self.profile_converted_)

    @cached_property
    def scores_(self) -> NiceDict:
        matrix = self.matrix_majority_
        return NiceDict({c: sum([v for (i, j), v in matrix.as_dict_.items() if i == c and j != c])
                         for c in matrix.candidates_})
