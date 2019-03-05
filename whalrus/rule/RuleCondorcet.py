from whalrus.rule.Rule import Rule
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property, NiceSet
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixMajority import MatrixMajority
from typing import Union


class RuleCondorcet(Rule):
    """
    Condorcet Rule.

    :param default_converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_majority: the majority matrix. Default: :class:`MatrixMajority`.

    If there is a Condorcet winner, then it it the winner and all other candidates are tied. If there is no Condorcet
    winner, then all candidates are tied.

    >>> RuleCondorcet(ballots=['a > b > c', 'b > a > c', 'c > a > b']).order_
    [{'a'}, {'b', 'c'}]
    >>> RuleCondorcet(ballots=['a > b > c', 'b > c > a', 'c > a > b']).order_
    [{'a', 'b', 'c'}]

    In all generality, a candidate is considered a `Condorcet winner' if all the non-diagonal coefficients on its raw of
    ``matrix_majority`` are equal to 1. With the default setting of ``matrix_majority = MatrixMajority()``, the
    `Condorcet winner' is necessarily unique when it exists, but that might not be the case with more exotic settings:

    >>> rule = RuleCondorcet(ballots=['a ~ b > c'], matrix_majority=MatrixMajority(equal=1.))
    >>> rule.matrix_majority_.as_df_
         a    b    c
    a  1.0  1.0  1.0
    b  1.0  1.0  1.0
    c  0.0  0.0  1.0
    >>> rule.order_
    [{'a', 'b'}, {'c'}]
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
    def order_(self) -> list:
        matrix = self.matrix_majority_
        condorcet_winners = {c for c in matrix.candidates_
                             if min({v for (i, j), v in matrix.as_dict_.items() if i == c and j != c}) == 1.}
        other_candidates = self.candidates_ - condorcet_winners
        return [NiceSet(tie_class) for tie_class in [condorcet_winners, other_candidates] if tie_class]
