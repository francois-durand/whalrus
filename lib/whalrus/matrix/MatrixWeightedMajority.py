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
from whalrus.utils.Utils import cached_property, NiceDict, convert_number, my_division
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union
from whalrus.matrix.Matrix import Matrix
from numbers import Number
from fractions import Fraction


class MatrixWeightedMajority(Matrix):
    """
    The weighted majority matrix.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param higher_vs_lower: number of points for candidate `c` when it is ordered higher than candidate `d`.
    :param lower_vs_higher: number of points for candidate `c` when it is ordered lower than candidate `d`.
    :param indifference: number of points for candidate `c` when it is ordered and tied with candidate `d`.
    :param ordered_vs_unordered: number of points for candidate `c` when it is ordered and `d` is unordered.
    :param unordered_vs_ordered: number of points for candidate `c` when it is unordered and `d` is ordered.
    :param unordered_vs_unordered: number of points for candidate `c` when it is unordered and `d` is unordered.
    :param ordered_vs_absent: number of points for candidate `c` when it is ordered and `d` is absent.
    :param absent_vs_ordered: number of points for candidate `c` when it is absent and `d` is ordered.
    :param unordered_vs_absent: number of points for candidate `c` when it is unordered and `d` is absent.
    :param absent_vs_unordered: number of points for candidate `c` when it is absent and `d` is unordered.
    :param absent_vs_absent: number of points for candidate `c` when it is absent and `d` is absent.
    :param diagonal_score: value of the diagonal coefficients.
    :param default_score: default score in the matrix in case of division by 0 (except for the diagonal coefficients).
    :param antisymmetric: if True, then an antisymmetric version of the matrix is computed (by subtracting the
        transposed matrix at the end of the computation).
    :param `**kwargs`: cf. parent class.

    In the most general syntax, firstly, you define the matrix computation algorithm:

    >>> matrix = MatrixWeightedMajority(diagonal_score=.5)

    Secondly, you use it as a callable to load a particular election (profile, candidates):

    >>> matrix(ballots=['a > b', 'b > a'], weights=[3, 1], voters=['v', 'w'], candidates={'a', 'b'})  # doctest:+ELLIPSIS
    <... object at ...>

    Finally, you can access the computed variables:

    >>> matrix.as_array_
    array([[Fraction(1, 2), Fraction(3, 4)],
           [Fraction(1, 4), Fraction(1, 2)]], dtype=object)

    Later, if you wish, you can load another profile with the same matrix computation algorithm, and so on.

    Optionally, you can specify an election (profile and candidates) as soon as the :class:`Matrix` object is
    initialized. This allows for "one-liners" such as:

    >>> MatrixWeightedMajority(ballots=['a > b', 'b > a'], weights=[3, 1], voters=['x', 'y'],
    ...                        candidates={'a', 'b'}, diagonal_score=.5).as_array_
    array([[Fraction(1, 2), Fraction(3, 4)],
           [Fraction(1, 4), Fraction(1, 2)]], dtype=object)

    Antisymmetric version:

    >>> MatrixWeightedMajority(ballots=['a > b', 'b > a'], weights=[3, 1], voters=['x', 'y'],
    ...                        candidates={'a', 'b'}, antisymmetric=True).as_array_
    array([[0, Fraction(1, 2)],
           [Fraction(-1, 2), 0]], dtype=object)

    An "unordered" candidate is a candidate that the voter has seen but not included in her ranking; i.e. it is in the
    attribute :attr:`BallotOrder.candidates_not_in_b` of the ballot. An "absent" candidate is a candidate that the
    voter has not even seen; i.e. it is in ``self.candidates_``, but not the attribute :attr:`Ballot.candidates` of the
    ballot. For all the "scoring" parameters (from ``higher_vs_lower`` to ``absent_vs_absent``), the value None can
    be used. In that case, the corresponding occurrences are not taken into account in the average (neither the
    numerator, not the denominator). Consider this example:

    >>> ballots = ['a > b', 'a ~ b']

    With ``indifference=Fraction(1, 2)`` (default), the ratio of voters who prefer `a` to `b` is
    (1 + 1 / 2) / 2 = 3 / 4 (the indifferent voter gives 1 / 2 point and is counted in the denominator):

    >>> MatrixWeightedMajority(ballots).as_array_
    array([[0, Fraction(3, 4)],
           [Fraction(1, 4), 0]], dtype=object)

    With ``indifference=0``, the ratio of voters who prefer `a` to `b` is 1 / 2 (the indifferent voter
    gives no point, but is counted in the denominator):

    >>> MatrixWeightedMajority(ballots, indifference=0).as_array_
    array([[0, Fraction(1, 2)],
           [0, 0]], dtype=object)

    With ``indifference=None``, the ratio of voters who prefer `a` to `b` is 1 / 1 = 1 (the indifferent voter is not
    counted in the average at all):

    >>> MatrixWeightedMajority(ballots, indifference=None).as_array_
    array([[0, 1],
           [0, 0]])
    """

    def __init__(self, *args,
                 converter: ConverterBallot = None,
                 higher_vs_lower: Union[Number, None] = 1, lower_vs_higher: Union[Number, None] = 0,
                 indifference: Union[Number, None] = Fraction(1, 2),
                 ordered_vs_unordered: Union[Number, None] = 1, unordered_vs_ordered: Union[Number, None] = 0,
                 unordered_vs_unordered: Union[Number, None] = Fraction(1, 2),
                 ordered_vs_absent: Union[Number, None] = None, absent_vs_ordered: Union[Number, None] = None,
                 unordered_vs_absent: Union[Number, None] = None, absent_vs_unordered: Union[Number, None] = None,
                 absent_vs_absent: Union[Number, None] = None,
                 diagonal_score: Number = 0, default_score: Number = 0, antisymmetric: bool = False, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        self.higher_vs_lower = convert_number(higher_vs_lower)
        self.lower_vs_higher = convert_number(lower_vs_higher)
        self.indifference = convert_number(indifference)
        self.ordered_vs_unordered = convert_number(ordered_vs_unordered)
        self.unordered_vs_ordered = convert_number(unordered_vs_ordered)
        self.unordered_vs_unordered = convert_number(unordered_vs_unordered)
        self.ordered_vs_absent = convert_number(ordered_vs_absent)
        self.absent_vs_ordered = convert_number(absent_vs_ordered)
        self.unordered_vs_absent = convert_number(unordered_vs_absent)
        self.absent_vs_unordered = convert_number(absent_vs_unordered)
        self.absent_vs_absent = convert_number(absent_vs_absent)
        self.diagonal_score = convert_number(diagonal_score)
        self.default_score = convert_number(default_score)
        self.antisymmetric = antisymmetric
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def _gross_and_weights_(self):
        gross = NiceDict({(c, d): 0 for c in self.candidates_ for d in self.candidates_})
        weights = NiceDict({(c, d): 0 for c in self.candidates_ for d in self.candidates_})
        for ballot, weight, _ in self.profile_converted_.items():
            absent = self.candidates_ - ballot.candidates
            for i_class, indifference_class in enumerate(ballot.as_weak_order):
                indifference_class_as_list = list(indifference_class)
                for i, c in enumerate(indifference_class_as_list):
                    # Deal with other candidates of the indifference class
                    if self.indifference is not None:
                        for d in indifference_class_as_list[i + 1:]:
                            gross[(c, d)] += weight * self.indifference
                            gross[(d, c)] += weight * self.indifference
                            weights[(c, d)] += weight
                            weights[(d, c)] += weight
                    # Deal with ordered candidates with lower ranks
                    if self.higher_vs_lower is not None or self.lower_vs_higher is not None:
                        for lower_indifference_class in ballot.as_weak_order[i_class + 1:]:
                            for d in lower_indifference_class:
                                if self.higher_vs_lower is not None:
                                    gross[(c, d)] += weight * self.higher_vs_lower
                                    weights[(c, d)] += weight
                                if self.lower_vs_higher is not None:
                                    gross[(d, c)] += weight * self.lower_vs_higher
                                    weights[(d, c)] += weight
                    # Deal with unordered candidates
                    if self.ordered_vs_unordered is not None or self.unordered_vs_ordered is not None:
                        for d in ballot.candidates_not_in_b:
                            if self.ordered_vs_unordered is not None:
                                gross[(c, d)] += weight * self.ordered_vs_unordered
                                weights[(c, d)] += weight
                            if self.unordered_vs_ordered is not None:
                                gross[(d, c)] += weight * self.unordered_vs_ordered
                                weights[(d, c)] += weight
                    # Deal with absent candidates
                    if self.ordered_vs_absent is not None or self.absent_vs_ordered is not None:
                        for d in absent:
                            if self.ordered_vs_absent is not None:
                                gross[(c, d)] += weight + self.ordered_vs_absent
                                weights[(c, d)] += weight
                            if self.absent_vs_ordered is not None:
                                gross[(d, c)] += weight + self.absent_vs_ordered
                                weights[(d, c)] += weight
            if (self.unordered_vs_unordered is not None
                    or self.unordered_vs_absent is not None
                    or self.absent_vs_unordered is not None):
                unordered_as_list = list(ballot.candidates_not_in_b)
                for i, c in enumerate(unordered_as_list):
                    # Deal with other unordered candidates
                    if self.unordered_vs_unordered is not None:
                        for d in unordered_as_list[i + 1:]:
                            gross[(c, d)] += weight * self.unordered_vs_unordered
                            gross[(d, c)] += weight * self.unordered_vs_unordered
                            weights[(c, d)] += weight
                            weights[(d, c)] += weight
                    # Deal with absent candidates
                    for d in absent:
                        if self.unordered_vs_absent is not None:
                            gross[(c, d)] += weight * self.unordered_vs_absent
                            weights[(c, d)] += weight
                        if self.absent_vs_unordered is not None:
                            gross[(d, c)] += weight * self.absent_vs_unordered
                            weights[(d, c)] += weight
            if self.absent_vs_absent is not None:
                absent_as_list = list(absent)
                for i, c in enumerate(absent_as_list):
                    for d in absent_as_list[i + 1:]:
                        gross[(c, d)] += weight * self.absent_vs_absent
                        gross[(d, c)] += weight * self.absent_vs_absent
                        weights[(c, d)] += weight
                        weights[(d, c)] += weight
        return {'gross': gross, 'weights': weights}

    @cached_property
    def gross_(self):
        """

        The "gross" matrix.

        :return: a NiceDict. Keys are pairs of candidates. Each coefficient is the weighted number of points (used as
            numerator in the average).

        >>> from whalrus import MatrixWeightedMajority
        >>> MatrixWeightedMajority(ballots=['a > b', 'a ~ b'], weights=[2, 1]).gross_
        {('a', 'a'): 0, ('a', 'b'): Fraction(5, 2), ('b', 'a'): Fraction(1, 2), ('b', 'b'): 0}
        """
        return self._gross_and_weights_['gross']

    @cached_property
    def weights_(self):
        """
        The matrix of weights.

        :return: a NiceDict. Keys are pairs of candidates. Each coefficient is the total weight (used as
            denominator in the average).

        In most usual cases, all non-diagonal coefficients are equal, and are equal to the total weight of all voters:

        >>> from whalrus import MatrixWeightedMajority
        >>> MatrixWeightedMajority(ballots=['a > b', 'a ~ b'], weights=[2, 1]).weights_
        {('a', 'a'): 0, ('a', 'b'): 3, ('b', 'a'): 3, ('b', 'b'): 0}

        However, if some scoring parameters are None, some weights can be lower than the total weight of all voters:

        >>> from whalrus import MatrixWeightedMajority
        >>> MatrixWeightedMajority(ballots=['a > b', 'a ~ b'], weights=[2, 1],
        ...                        indifference=None).weights_
        {('a', 'a'): 0, ('a', 'b'): 2, ('b', 'a'): 2, ('b', 'b'): 0}
        """
        return self._gross_and_weights_['weights']

    @cached_property
    def as_dict_(self):
        net_matrix = {
            (c, d): self.diagonal_score if c == d else my_division(
                self.gross_[(c, d)], w, divide_by_zero=self.default_score)
            for (c, d), w in self.weights_.items()}
        if self.antisymmetric:
            return {(c, d): net_matrix[(c, d)] - net_matrix[(d, c)] for (c, d) in net_matrix.keys()}
        else:
            return net_matrix
