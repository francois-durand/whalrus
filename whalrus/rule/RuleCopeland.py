from whalrus.rule.RuleScore import RuleScore
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property, NiceSet, NiceDict
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixMajority import MatrixMajority
from typing import Union


class RuleCopeland(RuleScore):
    """
    Copeland's rule.

    :param default_converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_majority: the majority matrix. Default: :class:`MatrixMajority`.

    The score of a candidate is the number of victories in the majority matrix. More exactly, it is the sum of
    the non-diagonal elements of its rows in the matrix.

    >>> rule = RuleCopeland(ballots=['a > b > c', 'b > a > c', 'c > a > b'])
    >>> rule.matrix_majority_.as_df_
         a    b    c
    a  0.5  1.0  1.0
    b  0.0  0.5  1.0
    c  0.0  0.0  0.5
    >>> rule.scores_
    {'a': 2.0, 'b': 1.0, 'c': 0.0}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, default_converter: ConverterBallot = None,
                 matrix_majority: Matrix = None):
        if default_converter is None:
            default_converter = ConverterBallotToOrder()
        if matrix_majority is None:
            matrix_majority = MatrixMajority()
        self.matrix_majority = matrix_majority
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter
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
