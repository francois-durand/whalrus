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
from whalrus.matrices.matrix_weighted_majority import MatrixWeightedMajority


class RuleMaximin(RuleScoreNum):
    """
    Maximin rule. Also known as Simpson-Kramer rule.

    The score of a candidate is the minimal non-diagonal coefficient on its raw of the matrix.

    Parameters
    ----------
    args
        Cf. parent class.
    converter : ConverterBallot
        Default: :class:`ConverterBallotToOrder`.
    matrix_weighted_majority : Matrix
        Default: :class:`MatrixWeightedMajority`.
    kwargs
        Cf. parent class.

    Examples
    --------
        >>> rule = RuleMaximin(ballots=['a > b > c', 'b > c > a', 'c > a > b'], weights=[4, 3, 3])
        >>> rule.matrix_weighted_majority_.as_array_of_floats_
        array([[0. , 0.7, 0.4],
               [0.3, 0. , 0.7],
               [0.6, 0.3, 0. ]])
        >>> rule.scores_as_floats_
        {'a': 0.4, 'b': 0.3, 'c': 0.3}
        >>> rule.winner_
        'a'
    """

    def __init__(self, *args, converter: ConverterBallot = None, matrix_weighted_majority: Matrix = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_weighted_majority is None:
            matrix_weighted_majority = MatrixWeightedMajority()
        self.matrix_weighted_majority = matrix_weighted_majority
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def matrix_weighted_majority_(self):
        """Matrix: The weighted majority matrix (once computed with the given profile).
        """
        return self.matrix_weighted_majority(self.profile_converted_)

    @cached_property
    def scores_(self) -> NiceDict:
        matrix = self.matrix_weighted_majority_
        return NiceDict({c: min({v for (i, j), v in matrix.as_dict_.items() if i == c and j != c})
                         for c in matrix.candidates_})
