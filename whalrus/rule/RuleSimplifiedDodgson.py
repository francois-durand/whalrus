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
from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property, NiceDict, convert_number
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixWeightedMajority import MatrixWeightedMajority


class RuleSimplifiedDodgson(RuleScoreNum):
    """
    Simplified Dodgson rule.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_weighted_majority: a :class:`Matrix`. Default: :class:`MatrixWeightedMajority` with
        ``antisymmetric=True``.
    :param `**kwargs`: cf. parent class.

    The score of a candidate is the sum of the negative non-diagonal coefficient on its raw of
    :attr:`matrix_weighted_majority_`.

    >>> rule = RuleSimplifiedDodgson(ballots=['a > b > c', 'b > a > c', 'c > a > b'],
    ...                              weights=[3, 3, 2])
    >>> rule.matrix_weighted_majority_.as_array_
    array([[0, Fraction(1, 4), Fraction(1, 2)],
           [Fraction(-1, 4), 0, Fraction(1, 2)],
           [Fraction(-1, 2), Fraction(-1, 2), 0]], dtype=object)
    >>> rule.scores_
    {'a': 0, 'b': Fraction(-1, 4), 'c': -1}
    >>> rule.winner_
    'a'
    """

    def __init__(self, *args, converter: ConverterBallot = None, matrix_weighted_majority: Matrix = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_weighted_majority is None:
            matrix_weighted_majority = MatrixWeightedMajority(antisymmetric=True)
        self.matrix_weighted_majority = matrix_weighted_majority
        super().__init__(*args, converter=converter, **kwargs)

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
        return NiceDict({
            c: convert_number(sum([v for (i, j), v in matrix.as_dict_.items() if i == c and j != c and v < 0]))
            for c in matrix.candidates_})
