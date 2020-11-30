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
from whalrus.rules.rule_score_num_row_sum import RuleScoreNumRowSum
from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
from whalrus.utils.utils import cached_property
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.matrices.matrix import Matrix
from whalrus.matrices.matrix_majority import MatrixMajority


class RuleCopeland(RuleScoreNumRowSum):
    """
    Copeland's rule.

    Parameters
    ----------
    args
        Cf. parent class.
    converter : ConverterBallot
        Default: :class:`ConverterBallotToOrder`.
    matrix : Matrix
        Default: :class:`MatrixMajority`.
    kwargs
        Cf. parent class.

    Examples
    --------
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
        """Matrix: The majority matrix. This is an alias for :attr:`matrix_`.

        Examples
        --------
            >>> rule = RuleCopeland(ballots=['a > b > c', 'b > a > c', 'c > a > b'])
            >>> rule.matrix_majority_.as_array_
            array([[Fraction(1, 2), 1, 1],
                   [0, Fraction(1, 2), 1],
                   [0, 0, Fraction(1, 2)]], dtype=object)
        """
        return self.matrix_
