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
from whalrus.rule.RuleScoreNumRowSum import RuleScoreNumRowSum
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixMajority import MatrixMajority


class RuleCopeland(RuleScoreNumRowSum):
    """
    Copeland's rule.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix: the default is :class:`MatrixMajority`.
    :param `**kwargs`: cf. parent class.

    The score of a candidate is the number of victories in the majority matrix.

    >>> rule = RuleCopeland(ballots=['a > b > c', 'b > a > c', 'c > a > b'])
    >>> rule.matrix_.as_array_
    array([[Fraction(1, 2), 1, 1],
           [0, Fraction(1, 2), 1],
           [0, 0, Fraction(1, 2)]], dtype=object)
    >>> rule.scores_
    {'a': 2, 'b': 1, 'c': 0}
    """

    def __init__(self, *args, converter: ConverterBallot = None, matrix: Matrix = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix is None:
            matrix = MatrixMajority()
        super().__init__(*args, converter=converter, matrix=matrix, **kwargs)

    @cached_property
    def matrix_majority_(self):
        """
        The majority matrix.

        :return: alias for :attr:`matrix_`.
        """
        return self.matrix_
