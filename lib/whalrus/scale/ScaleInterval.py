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
from whalrus.scale.Scale import Scale
from whalrus.utils.Utils import convert_number
from typing import Iterable
from numbers import Number


class ScaleInterval(Scale):
    """
    A scale given by a continuous interval of numbers.

    :param low: lowest grade.
    :param high: highest grade.

    >>> ScaleInterval(low=0, high=2.5)
    ScaleInterval(low=0, high=Fraction(5, 2))
    """

    def __init__(self, low: Number = 0, high: Number = 1):
        self._low = convert_number(low)
        self._high = convert_number(high)

    @property
    def low(self) -> object:
        """
        >>> ScaleInterval(low=0, high=1).low
        0
        """
        return self._low

    @property
    def high(self) -> object:
        """
        >>> ScaleInterval(low=0, high=1).high
        1
        """
        return self._high

    @property
    def is_bounded(self) -> bool:
        return True

    def __repr__(self):
        return 'ScaleInterval(low=%r, high=%r)' % (self.low, self.high)

    # Min, max and sort
    # -----------------

    def min(self, iterable: Iterable) -> object:
        """
        >>> ScaleInterval(low=0, high=1).min([.3, .1, .7])
        0.1
        """
        return min(iterable)

    def max(self, iterable: Iterable) -> object:
        """
        >>> ScaleInterval(low=0, high=1).max([.3, .1, .7])
        0.7
        """
        return max(iterable)

    # noinspection PyMethodMayBeStatic
    def sort(self, some_list: list, reverse: bool = False) -> None:
        """
        >>> some_list = [.3, .1, .7]
        >>> ScaleInterval(low=0, high=1).sort(some_list)
        >>> some_list
        [0.1, 0.3, 0.7]
        """
        some_list.sort(reverse=reverse)

    def argsort(self, some_list: list, reverse: bool = False) -> list:
        """
        >>> ScaleInterval(low=0, high=1).argsort([.3, .1, .7])
        [1, 0, 2]
        """
        return sorted(range(len(some_list)), key=lambda i: some_list[i], reverse=reverse)
