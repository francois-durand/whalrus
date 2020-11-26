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
from whalrus.priority.Priority import Priority
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixWeightedMajority import MatrixWeightedMajority
import numpy as np
from itertools import chain


class MatrixRankedPairs(Matrix):
    """
    The ranked pairs matrix.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_weighted_majority: a :class:`Matrix`. Algorithm used to compute the weighted majority matrix `W`.
        Default: :class:`MatrixWeightedMajority`.
    :param tie_break: a :class:`Priority`. The tie-break used when two duels have the same score.
    :param `**kwargs`: cf. parent class.

    First, we compute a matrix `W` with the algorithm given in the parameter ``matrix_weighted_majority``.
    The ranked pair matrix represents a graph whose vertices are the candidates. In order to build it, we consider
    all duels between two distinct candidates `(c, d)`, by decreasing order of the value `W(c, d)`. We add an edge
    `(c, d)` in the ranked pairs matrix, except if it creates a cycle in the graph, and we consider the transitive
    closure.

    >>> m = MatrixRankedPairs(['a > b > c', 'b > c > a', 'c > a > b'], weights=[4, 3, 2])
    >>> m.edges_order_
    [('b', 'c'), ('a', 'b'), ('c', 'a')]
    >>> m.as_array_
    array([[0, 1, 1],
           [0, 0, 1],
           [0, 0, 0]], dtype=object)

    In the example example above, the edge `(b, c)` is added. Then it is the edge `(a, b)` which, by transitive closure,
    also adds the edge `(a, c)`. Finally the edge `(c, a)` (representing the victory of `c` over `a` in the weighted
    majority matrix) should be added, but it would introduce a cycle in the graph, so it is ignored.

    If two duels have the same score, the tie-break is used. For example, with :attr:`Priority.ASCENDING`, we add a
    victory `(a, ...)` before a victory `(b, ...)`; and we add a victory `(a, c)` before a victory `(a, b)` (because
    `b` is favored over `c`). A very simple but illustrative example:

    >>> MatrixRankedPairs(['a > b > c'], tie_break=Priority.ASCENDING).edges_order_
    [('a', 'c'), ('a', 'b'), ('b', 'c')]
    """

    def __init__(self, *args, converter: ConverterBallot = None, matrix_weighted_majority: Matrix = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_weighted_majority is None:
            matrix_weighted_majority = MatrixWeightedMajority()
        self.tie_break = tie_break
        self.matrix_weighted_majority = matrix_weighted_majority
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def matrix_weighted_majority_(self):
        """
        The weighted majority matrix (upon which the computation of the Ranked Pairs matrix is based).

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
    def edges_order_(self) -> list:
        """
        The order in which edges should be added (if possible).

        :return: a list of pairs of candidates. E.g. ``[('b', 'c'), ('c', 'a'), ('a', 'b')]``, where ('b', 'c') is the
            first edge to add.
        """
        m = self.matrix_weighted_majority_
        return list(chain(*[
            self.tie_break.sort_pairs_rp({
                (c, d) for (c, d), v in m.as_dict_.items()
                if v == value and c != d and m.as_dict_[(c, d)] >= m.as_dict_[(d, c)]
            })
            for value in sorted(set(m.as_dict_.values()), reverse=True)
        ]))

    @cached_property
    def as_array_(self):
        n = len(self.candidates_)
        rp = np.zeros((n, n), dtype=object)
        for (c, d) in self.edges_order_:
            i = self.matrix_weighted_majority_.candidates_indexes_[c]
            j = self.matrix_weighted_majority_.candidates_indexes_[d]
            if rp[j, i] > 0:
                continue
            rp[i, j] = 1
            rp[i, :] = np.maximum(rp[i, :], rp[j, :])
            rp[:, j] = np.maximum(rp[:, i], rp[:, j])
        return rp

    @cached_property
    def as_dict_(self):
        return NiceDict({(c, d): self.as_array_[self.candidates_indexes_[c], self.candidates_indexes_[d]]
                         for c in self.candidates_ for d in self.candidates_})
