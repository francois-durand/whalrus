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
from typing import Iterable


class ScaleRange(Scale):
    """
    A scale of consecutive integers.

    :param low: lowest integer.
    :param high: highest integer.

    Remark: for a scale of non-consecutive integers, such as {-1, 0, 2}, use the :class:`ScaleFromSet`.

    >>> scale = ScaleRange(low=0, high=5)
    """

    def __init__(self, low: int, high: int):
        self._low = low
        self._high = high

    @property
    def low(self) -> int:
        """
        >>> ScaleRange(low=0, high=5).low
        0
        """
        return self._low

    @property
    def high(self) -> int:
        """
        >>> ScaleRange(low=0, high=5).high
        5
        """
        return self._high

    @property
    def is_bounded(self) -> bool:
        return True

    def __repr__(self):
        return 'ScaleRange(low=%s, high=%s)' % (self.low, self.high)

    # Min, max and sort
    # -----------------

    def min(self, iterable: Iterable) -> object:
        """
        >>> ScaleRange(low=0, high=5).min([3, 1, 4])
        1
        """
        return min(iterable)

    def max(self, iterable: Iterable) -> object:
        """
        >>> ScaleRange(low=0, high=5).max([3, 1, 4])
        4
        """
        return max(iterable)

    # noinspection PyMethodMayBeStatic
    def sort(self, some_list: list, reverse: bool = False) -> None:
        """
        >>> some_list = [3, 1, 4]
        >>> ScaleRange(low=0, high=5).sort(some_list)
        >>> some_list
        [1, 3, 4]
        """
        some_list.sort(reverse=reverse)

    def argsort(self, some_list: list, reverse: bool = False) -> list:
        """
        >>> ScaleRange(low=0, high=5).argsort([3, 1, 4])
        [1, 0, 2]
        """
        return sorted(range(len(some_list)), key=lambda i: some_list[i], reverse=reverse)
