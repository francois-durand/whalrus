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
from whalrus.rules.rule_score_num import RuleScoreNum
from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
from whalrus.utils.utils import cached_property, NiceDict
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.matrices.matrix import Matrix


class RuleScoreNumRowSum(RuleScoreNum):
    """
    Rule where the winner is the candidate having the highest row sum in some matrix.

    The score of a candidate is the sum of the non-diagonal elements of its row in :attr:`matrix_`.

    Parameters
    ----------
    args
        Cf. parent class.
    matrix : Matrix
        The matrix upon which the scores are based.
    kwargs
        Cf. parent class.
    """

    def __init__(self, *args, matrix: Matrix = None, **kwargs):
        self.matrix = matrix
        super().__init__(*args, **kwargs)

    @cached_property
    def matrix_(self):
        """Matrix: The matrix (once computed with the given profile).
        """
        return self.matrix(self.profile_converted_)

    @cached_property
    def scores_(self) -> NiceDict:
        m = self.matrix_
        return NiceDict({c: sum([v for (i, j), v in m.as_dict_.items() if i == c and j != c])
                         for c in m.candidates_})
