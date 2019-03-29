# -*- coding: utf-8 -*-
"""
Copyright Sylvain Bouveret, Yann Chevaleyre and François Durand
sylvain.bouveret@imag.fr, yann.chevaleyre@dauphine.fr, fradurand@gmail.com

This file is part of Whalrus.

Whalrus is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Whalrus is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Whalrus.  If not, see <http://www.gnu.org/licenses/>.
"""
from whalrus.utils.Utils import cached_property, NiceDict, convert_number
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixWeightedMajority import MatrixWeightedMajority
from numbers import Number
from fractions import Fraction


class MatrixMajority(Matrix):
    """
    The majority matrix.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_weighted_majority: a :class:`Matrix`. Algorithm used to compute the weighted majority matrix `W`.
        Default: :class:`MatrixWeightedMajority`.
    :param greater: value used when `W(c, d) > W(d, c)`.
    :param lower: value used when `W(c, d) < W(d, c)`.
    :param equal: value used when `W(c, d) = W(d, c)` (except for diagonal coefficients).
    :param diagonal: value used for the diagonal coefficients.
    :param `**kwargs`: cf. parent class.

    First, we compute a matrix `W` with the algorithm given in the parameter ``matrix_weighted_majority``.
    Then for each pair of candidates `(c, d)`, the coefficient of the majority matrix is set to :attr:`greater`,
    :attr:`lower`, :attr:`equal` or :attr:`diagonal`, depending on the values of `W(c, d)` and `W(d, c)`.

    >>> MatrixMajority(ballots=['a > b ~ c', 'b > a > c', 'c > a > b']).as_array_
    array([[Fraction(1, 2), 1, 1],
           [0, Fraction(1, 2), Fraction(1, 2)],
           [0, Fraction(1, 2), Fraction(1, 2)]], dtype=object)

    Using the options:

    >>> MatrixMajority(ballots=['a > b ~ c', 'b > a > c', 'c > a > b'], equal=0, diagonal=0).as_array_
    array([[0, 1, 1],
           [0, 0, 0],
           [0, 0, 0]])
    """

    def __init__(self, *args, converter: ConverterBallot = None, matrix_weighted_majority: Matrix = None,
                 greater: Number = 1, lower: Number = 0, equal: Number = Fraction(1, 2),
                 diagonal: Number = Fraction(1, 2), **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_weighted_majority is None:
            matrix_weighted_majority = MatrixWeightedMajority()
        self.matrix_weighted_majority = matrix_weighted_majority
        self.greater = convert_number(greater)
        self.lower = convert_number(lower)
        self.equal = convert_number(equal)
        self.diagonal = convert_number(diagonal)
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def matrix_weighted_majority_(self):
        """
        The weighted majority matrix (upon which the computation of the majority matrix is based).

        :return: the weighted majority matrix (once computed with the given profile).
        """
        return self.matrix_weighted_majority(self.profile_converted_)

    @cached_property
    def candidates_as_list_(self) -> list:
        return self.matrix_weighted_majority_.candidates_as_list_

    @cached_property
    def candidates_indexes_(self) -> NiceDict:
        return self.matrix_weighted_majority_.candidates_indexes_

    @cached_property
    def as_dict_(self):
        def convert(x, y):
            if x == y:
                return self.equal
            return self.greater if x > y else self.lower
        weighted_as_dict = self.matrix_weighted_majority_.as_dict_
        return NiceDict({
            (c, d): self.diagonal if c == d else convert(weighted_as_dict[(c, d)], weighted_as_dict[(d, c)])
            for (c, d) in weighted_as_dict.keys()
        })
