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
from functools import cmp_to_key
from typing import Iterable


class Scale:
    """
    A scale used to evaluate the candidates (for :class:`RuleRangeVoting`, :class:`RuleMajorityJudgment`, etc).

    This parent class represents a generic scale, where two levels of the scale compare according to their internal
    methods ``__lt__``, ``__le__``, etc.

    For a subclass, it is sufficient to override the method :meth:`lt` and the other comparison methods will be
    modified accordingly (assuming it describes a total order).

    >>> scale = Scale()
    >>> scale.lt(1, 7)
    True
    """

    # noinspection PyMethodMayBeStatic
    def eq(self, one: object, another: object) -> bool:
        """
        Test "equal". Cf. :meth:`lt`.
        """
        return one == another

    # noinspection PyMethodMayBeStatic
    def ne(self, one: object, another: object) -> bool:
        """
        Test "not equal". Cf. :meth:`lt`.
        """
        return not self.eq(one, another)

    # noinspection PyMethodMayBeStatic
    def lt(self, one: object, another: object) -> bool:
        """
        Test "lower than".

        :param one: a level of the scale.
        :param another: a level of the scale.
        :return: True iff :attr:`one` is lower than :attr:`another`.

        Generally, only this method is overridden in the subclasses.

        >>> Scale().lt('a', 'z')
        True
        """
        return one < another

    # noinspection PyMethodMayBeStatic
    def le(self, one: object, another: object) -> bool:
        """
        Test "lower or equal". Cf. :meth:`lt`.
        """
        return self.eq(one, another) or self.lt(one, another)

    # noinspection PyMethodMayBeStatic
    def gt(self, one: object, another: object) -> bool:
        """
        Test "greater than". Cf. :meth:`lt`.
        """
        return self.lt(another, one)

    # noinspection PyMethodMayBeStatic
    def ge(self, one: object, another: object) -> bool:
        """
        Test "greater or equal". Cf. :meth:`lt`.
        """
        return self.le(another, one)

    @property
    def low(self):
        """
        The lowest element of the scale.

        :return: the lowest element (or None if the scale is unbounded below).
        """
        return None

    @property
    def high(self):
        """
        The highest element of the scale.

        :return: the highest element (or None if the scale is unbounded above).
        """
        return None

    @property
    def is_bounded(self):
        return (self.low is not None) and (self.high is not None)

    def __repr__(self):
        return '%s()' % type(self).__name__

    # Min, max and sort
    # -----------------

    def compare(self, one: object, another: object) -> int:
        """
        Compare two levels.

        :param one: a level.
        :param another: a level.
        :return: 0 if they are equal, a positive number if ``one`` is greater than ``another``, a negative number
            otherwise.

        >>> Scale().compare('a', 'z')
        -1
        """
        if self.eq(one, another):
            return 0
        return -1 if self.lt(one, another) else 1

    def min(self, iterable: Iterable) -> object:
        """
        Minimum of some levels.

        :param iterable: an iterable of levels (list, set, etc).

        >>> Scale().min({'x', 'a', 'z'})
        'a'
        """
        return min(iterable, key=cmp_to_key(self.compare))

    def max(self, iterable: Iterable) -> object:
        """
        Maximum of some levels.

        :param iterable: an iterable of levels (list, set, etc).

        >>> Scale().max({4, 1, 12})
        12
        """
        return max(iterable, key=cmp_to_key(self.compare))

    def sort(self, some_list: list, reverse: bool = False) -> None:
        """
        Sort a list of levels (in place).

        :param some_list: a list of levels.
        :param reverse: if True, then sort in decreasing order.

        >>> some_list = [42, 3, 12]
        >>> Scale().sort(some_list)
        >>> some_list
        [3, 12, 42]
        """
        some_list.sort(key=cmp_to_key(self.compare), reverse=reverse)

    def argsort(self, some_list: list, reverse: bool = False) -> list:
        """
        "Argsort" a list of levels.

        :param some_list: a list of levels.
        :param reverse: if True, then argsort in decreasing order.
        :return: a list of indexes.

        >>> Scale().argsort(['a', 'c', 'b'])
        [0, 2, 1]
        """
        def compare_indexes(one: int, another: int) -> int:
            return self.compare(some_list[one], some_list[another])
        return sorted(range(len(some_list)), key=cmp_to_key(compare_indexes), reverse=reverse)
