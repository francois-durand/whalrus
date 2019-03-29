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
from whalrus.matrix.MatrixSchulze import MatrixSchulze


class RuleSchulze(Rule):
    """
    Schulze's Rule.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param matrix_schulze: the Schulze matrix. Default: :class:`MatrixSchulze`.
    :param `**kwargs`: cf. parent class.

    A candidate is a Schulze winner if it has no defeat in the Schulze matrix.

    >>> rule = RuleSchulze(['a > b > c', 'b > c > a', 'c > a > b'], weights=[4, 3, 2])
    >>> rule.matrix_schulze_.as_array_
    array([[0, Fraction(2, 3), Fraction(2, 3)],
           [Fraction(5, 9), 0, Fraction(7, 9)],
           [Fraction(5, 9), Fraction(5, 9), 0]], dtype=object)
    >>> rule.winner_
    'a'
    """

    def __init__(self, *args, converter: ConverterBallot = None, matrix_schulze: Matrix = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if matrix_schulze is None:
            matrix_schulze = MatrixSchulze()
        self.matrix_schulze = matrix_schulze
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def matrix_schulze_(self):
        """
        The Schulze matrix.

        :return: the Schulze matrix (once computed with the given profile).
        """
        return self.matrix_schulze(self.profile_converted_)

    @cached_property
    def order_(self) -> list:
        m = self.matrix_schulze_
        victories = {(c, d) for (c, d) in m.as_dict_.keys() if m.as_dict_[(c, d)] > m.as_dict_[(d, c)]}
        to_sort = self.candidates_.copy()
        result = []
        while to_sort:
            losers = {d for (c, d) in victories}
            result.append(to_sort - losers)
            to_sort = losers
            victories = {(c, d) for (c, d) in victories if c in to_sort and d in to_sort}
        return result
