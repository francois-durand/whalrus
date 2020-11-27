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
from whalrus.utils.utils import cached_property, NiceDict
from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.matrices.matrix import Matrix
from whalrus.matrices.matrix_weighted_majority import MatrixWeightedMajority
import numpy as np


class MatrixSchulze(Matrix):
    """
    The Schulze matrix.

    Parameters
    ----------
    args
        Cf. parent class.
    converter : ConverterBallot
        Default: :class:`ConverterBallotToOrder`.
    matrix_weighted_majority : Matrix
        Algorithm used to compute the weighted majority matrix `W`. Default: :class:`MatrixWeightedMajority`.
    kwargs
        Cf. parent class.

    Examples
    --------
    First, we compute a matrix `W` with the algorithm given in the parameter ``matrix_weighted_majority``.
    The Schulze matrix gives, for each pair of candidates `(c, d)`, the width of the widest path from `c` to `d`, where
    the width of a path is the minimum weight of its edges.

        >>> m = MatrixSchulze(['a > b > c', 'b > c > a', 'c > a > b'], weights=[4, 3, 2])
        >>> m.as_array_
        array([[0, Fraction(2, 3), Fraction(2, 3)],
               [Fraction(5, 9), 0, Fraction(7, 9)],
               [Fraction(5, 9), Fraction(5, 9), 0]], dtype=object)
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
        """Matrix: The weighted majority matrix (upon which the computation of the Schulze is based), once computed
        with the given profile.
        """
        return self.matrix_weighted_majority(self.profile_converted_)

    @cached_property
    def candidates_as_list_(self) -> list:
        return self.matrix_weighted_majority_.candidates_as_list_

    @cached_property
    def candidates_indexes_(self) -> NiceDict:
        return self.matrix_weighted_majority_.candidates_indexes_

    @cached_property
    def as_array_(self):
        widest_path = np.copy(self.matrix_weighted_majority_.as_array_)
        n = len(self.candidates_)
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                for k in range(n):
                    if k == i or k == j:
                        continue
                    widest_path[j, k] = max(widest_path[j, k], min(widest_path[j, i], widest_path[i, k]))
        return widest_path

    @cached_property
    def as_dict_(self):
        return NiceDict({(c, d): self.as_array_[self.candidates_indexes_[c], self.candidates_indexes_[d]]
                         for c in self.candidates_ for d in self.candidates_})
