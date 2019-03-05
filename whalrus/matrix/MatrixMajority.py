from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixWeightedMajority import MatrixWeightedMajority


class MatrixMajority(Matrix):
    """

    :param default_converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_weighted_majority: a :class:`Matrix`. Default: :class:`MatrixWeightedMajority`.
    :param greater: value when in the weighted matrix, coefficient ``(c, d)`` is greater than coefficient ``(d, c)``.
    :param lower: value when in the weighted matrix, coefficient ``(c, d)`` is lower than coefficient ``(d, c)``.
    :param equal: value when in the weighted matrix, coefficient ``(c, d)`` is equal to coefficient ``(d, c)``.

    First, we compute a matrix ``W`` with the algorithm given in the parameter ``matrix_weighted_majority``.
    Then for each pair of candidates ``(c, d)``, the coefficient ``(c, d)`` of the majority matrix is set to
    :attr:`greater` if ``W[(d, c)] > W[(d, c)]``, :attr:`equal` if ``W[(d, c)] = W[(d, c)]`` and :attr:`lower` if `
    `W[(d, c)] < W[(d, c)]``.

    >>> MatrixMajority(ballots=['a > b ~ c', 'b > a > c', 'c > a > b']).as_df_
         a    b    c
    a  0.5  1.0  1.0
    b  0.0  0.5  0.5
    c  0.0  0.5  0.5

    Using the options:

    >>> MatrixMajority(ballots=['a > b ~ c', 'b > a > c', 'c > a > b'], equal=0.).as_df_
         a    b    c
    a  0.0  1.0  1.0
    b  0.0  0.0  0.0
    c  0.0  0.0  0.0
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None,
                 default_converter: ConverterBallot = None,
                 matrix_weighted_majority: Matrix = None,
                 greater: float = 1., lower: float = 0., equal: float = .5):
        if default_converter is None:
            default_converter = ConverterBallotToOrder()
        if matrix_weighted_majority is None:
            matrix_weighted_majority = MatrixWeightedMajority()
        self.matrix_weighted_majority = matrix_weighted_majority
        self.greater = greater
        self.lower = lower
        self.equal = equal
        super().__init__(ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
                         default_converter=default_converter)

    @cached_property
    def matrix_weighted_majority_(self):
        """
        The weighted majority matrix (upon which the computation of the majority matrix is based).

        :return: the weighted majority matrix (once computed with the given profile).
        """
        return self.matrix_weighted_majority(self.profile_converted_)

    @cached_property
    def as_dict_(self):
        def convert(x, y):
            if x == y:
                return self.equal
            return self.greater if x > y else self.lower
        weighted_as_dict = self.matrix_weighted_majority_.as_dict_
        return NiceDict({(c, d): convert(weighted_as_dict[(c, d)], weighted_as_dict[(d, c)])
                         for (c, d) in weighted_as_dict.keys()})
