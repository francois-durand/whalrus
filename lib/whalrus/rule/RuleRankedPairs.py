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
from whalrus.matrix.MatrixRankedPairs import MatrixRankedPairs


class RuleRankedPairs(RuleScoreNumRowSum):
    """
    Ranked Pairs rule.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix: the default is ``MatrixRankedPairs(tie_break=tie_break)``.
    :param `**kwargs`: cf. parent class.

    The score of a candidate is the number of victories in the ranked pairs matrix.

    >>> rule = RuleRankedPairs(['a > b > c', 'b > c > a', 'c > a > b'], weights=[4, 3, 2])
    >>> rule.matrix_.as_array_
    array([[0, 1, 1],
           [0, 0, 1],
           [0, 0, 0]], dtype=object)
    >>> rule.scores_
    {'a': 2, 'b': 1, 'c': 0}
    """

    def __init__(self, *args, converter: ConverterBallot = None, matrix: Matrix = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix is None:
            tie_break = kwargs.get('tie_break')
            if tie_break is None:
                matrix = MatrixRankedPairs()
            else:
                matrix = MatrixRankedPairs(tie_break=tie_break)
        super().__init__(*args, converter=converter, matrix=matrix, **kwargs)

    @cached_property
    def matrix_ranked_pairs_(self):
        """
        The ranked pairs matrix.

        :return: alias for :attr:`matrix_`.
        """
        return self.matrix_
