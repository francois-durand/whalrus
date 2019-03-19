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
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixWeightedMajority import MatrixWeightedMajority
from numbers import Number
from fractions import Fraction


class MatrixMajority(Matrix):
    """

    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_weighted_majority: a :class:`Matrix`. Default: :class:`MatrixWeightedMajority`.
    :param greater: value when in the weighted matrix, coefficient ``(c, d)`` is greater than coefficient ``(d, c)``.
    :param lower: value when in the weighted matrix, coefficient ``(c, d)`` is lower than coefficient ``(d, c)``.
    :param equal: value when in the weighted matrix, coefficient ``(c, d)`` is equal to coefficient ``(d, c)``.

    First, we compute a matrix ``W`` with the algorithm given in the parameter ``matrix_weighted_majority``.
    Then for each pair of candidates ``(c, d)``, the coefficient ``(c, d)`` of the majority matrix is set to
    :attr:`greater` if ``W[(d, c)] > W[(d, c)]``, :attr:`equal` if ``W[(d, c)] = W[(d, c)]`` and :attr:`lower` if `
    `W[(d, c)] < W[(d, c)]``.

    >>> MatrixMajority(ballots=['a > b ~ c', 'b > a > c', 'c > a > b']).as_array_
    array([[Fraction(1, 2), 1, 1],
           [0, Fraction(1, 2), Fraction(1, 2)],
           [0, Fraction(1, 2), Fraction(1, 2)]], dtype=object)

    Using the options:

    >>> MatrixMajority(ballots=['a > b ~ c', 'b > a > c', 'c > a > b'], equal=0).as_array_
    array([[0, 1, 1],
           [0, 0, 0],
           [0, 0, 0]])
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 converter: ConverterBallot = None,
                 matrix_weighted_majority: Matrix = None,
                 greater: Number = 1, lower: Number = 0, equal: Number = Fraction(1, 2)):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_weighted_majority is None:
            matrix_weighted_majority = MatrixWeightedMajority()
        self.matrix_weighted_majority = matrix_weighted_majority
        self.greater = convert_number(greater)
        self.lower = convert_number(lower)
        self.equal = convert_number(equal)
        super().__init__(ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter)

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
