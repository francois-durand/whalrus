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
from typing import Union
from whalrus.priority.Priority import Priority
from functools import cmp_to_key
# Ideally, all Union[set, list] in this file should be typing.Collection, but it is only defined in Python >= 3.6.


class LiftedSetPriority(Priority):
    """
    A set priority setting computed from lifting a priority on individual
    elements to a priority on sets of elements.

    :param name: the name of this priority setting.
    :param base_priority: the priority on single elements.

    :cvar MAX: shortcut for :class:`SetPriorityMax`.
    :cvar MIN: shortcut for :class:`SetPriorityMin`.
    :cvar RESPONSIVE: shortcut for :class:`SetPriorityResponsive`.
    """

    def __init__(self, name: str, base_priority=Priority.UNAMBIGUOUS):
        self.base_priority = Priority.UNAMBIGUOUS
        self.name = name

    LEXIMAX = None
    LEXIMIN = None


class LiftedSetPriorityLexico(LiftedSetPriority):
    """
    Abstract lexicographic order.
    """

    def _choice(self, x: Union[set, list], reverse: bool) -> object:
        if reverse:
            return max(x, key=cmp_to_key(self._lexico_cmp))
        return min(x, key=cmp_to_key(self._lexico_cmp))

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return sorted(x, key=cmp_to_key(self._lexico_cmp), reverse=reverse)

    def _lexico_cmp(self, s1, s2):
        raise NotImplementedError


class LiftedSetPriorityLeximax(LiftedSetPriorityLexico):
    """
    Lexicographic max order (best elements compared first, then
    second ones, and so on). If one set is included in another,
    the shortest is favoured.

    >>> priority = LiftedSetPriority.LEXIMAX
    >>> priority.base_priority=Priority.ASCENDING
    >>> priority.sort([['a', 'c', 'd'], ['a', 'b', 'e'], ['b', 'c'], ['a', 'b']])
    [['a', 'b'], ['a', 'b', 'e'], ['a', 'c', 'd'], ['b', 'c']]
    """

    def __init__(self, base_priority=Priority.UNAMBIGUOUS):
        super().__init__(name='LiftedLeximaxPriority',
                         base_priority=base_priority)

    def __repr__(self):
        return 'LiftedSetPriority.LEXIMAX'

    def _lexico_cmp(self, s1, s2):
        for a, b in zip(self.base_priority.sort(s1),
                        self.base_priority.sort(s2)):
            if a != b:
                return -1 if self.base_priority.choice([a, b]) == a else 1
        return len(s1) - len(s2)


LiftedSetPriority.LEXIMAX = LiftedSetPriorityLeximax()


class LiftedSetPriorityLeximin(LiftedSetPriorityLexico):
    """
    Lexicographic min order (worst elements compared first, then
    second ones, and so on). If one set is included in another,
    the shortest is favoured.

    >>> priority = LiftedSetPriority.LEXIMIN
    >>> priority.base_priority=Priority.ASCENDING
    >>> priority.sort([['a', 'c', 'd'], ['a', 'b', 'e'], ['b', 'c'], ['a', 'b']])
    [['a', 'b'], ['b', 'c'], ['a', 'c', 'd'], ['a', 'b', 'e']]
    """

    def __init__(self, base_priority=Priority.UNAMBIGUOUS):
        super().__init__(name='LiftedLeximinPriority',
                         base_priority=base_priority)

    def __repr__(self):
        return 'LiftedSetPriority.LEXIMIN'

    def _lexico_cmp(self, s1, s2):
        for a, b in zip(self.base_priority.sort(s1, reverse=True),
                        self.base_priority.sort(s2, reverse=True)):
            if a != b:
                return -1 if self.base_priority.choice([a, b]) == a else 1
        return len(s1) - len(s2)


LiftedSetPriority.LEXIMIN = LiftedSetPriorityLeximin()
