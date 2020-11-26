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
from whalrus.rule.Rule import Rule
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property, NiceSet
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.matrix.Matrix import Matrix
from whalrus.matrix.MatrixMajority import MatrixMajority


class RuleCondorcet(Rule):
    """
    Condorcet Rule.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_majority: the majority matrix. Default: :class:`MatrixMajority`.
    :param `**kwargs`: cf. parent class.

    If there is a Condorcet winner, then it it the winner and all other candidates are tied. If there is no Condorcet
    winner, then all candidates are tied.

    >>> RuleCondorcet(ballots=['a > b > c', 'b > a > c', 'c > a > b']).order_
    [{'a'}, {'b', 'c'}]
    >>> RuleCondorcet(ballots=['a > b > c', 'b > c > a', 'c > a > b']).order_
    [{'a', 'b', 'c'}]

    More precisely, and in all generality, a candidate is considered a `Condorcet winner` if all the non-diagonal
    coefficients on its raw of :attr:`matrix_majority_` are equal to 1. With the default setting of ``matrix_majority =
    MatrixMajority()``, the Condorcet winner is necessarily unique when it exists, but that might not be the case
    with some more exotic settings:

    >>> rule = RuleCondorcet(ballots=['a ~ b > c'], matrix_majority=MatrixMajority(equal=1))
    >>> rule.matrix_majority_.as_array_
    array([[Fraction(1, 2), 1, 1],
           [1, Fraction(1, 2), 1],
           [0, 0, Fraction(1, 2)]], dtype=object)
    >>> rule.order_
    [{'a', 'b'}, {'c'}]
    """

    def __init__(self, *args, converter: ConverterBallot = None, matrix_majority: Matrix = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_majority is None:
            matrix_majority = MatrixMajority()
        self.matrix_majority = matrix_majority
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def matrix_majority_(self):
        """
        The majority matrix.

        :return: the majority matrix (once computed with the given profile).
        """
        return self.matrix_majority(self.profile_converted_)

    @cached_property
    def order_(self) -> list:
        matrix = self.matrix_majority_
        condorcet_winners = {c for c in matrix.candidates_
                             if min({v for (i, j), v in matrix.as_dict_.items() if i == c and j != c}) == 1}
        other_candidates = self.candidates_ - condorcet_winners
        return [NiceSet(tie_class) for tie_class in [condorcet_winners, other_candidates] if tie_class]
