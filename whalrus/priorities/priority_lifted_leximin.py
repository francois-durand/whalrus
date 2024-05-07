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
from whalrus.priorities.priority import Priority
from whalrus.priorities.priority_lifted import PriorityLifted


class PriorityLiftedLeximin(PriorityLifted):
    """
    Lexicographic min order (worst elements compared first, then second ones, and so on). If one set is included in
    another, the shortest is favoured.

    >>> priority = PriorityLiftedLeximin(Priority.ASCENDING)
    >>> print(priority)
    Leximin(Ascending)
    >>> priority.sort_committees([['a', 'c', 'd'], ['a', 'b', 'e'], ['b', 'c'], ['a', 'b']])
    [['a', 'b'], ['b', 'c'], ['a', 'c', 'd'], ['a', 'b', 'e']]
    """

    def __init__(self, base_priority: Priority = Priority.UNAMBIGUOUS):
        super().__init__(name="Leximin(%s)" % base_priority.name, base_priority=base_priority)

    def compare_committees(self, s, t) -> int:
        for c, d in zip(self.base_priority.sort(s, reverse=True), self.base_priority.sort(t, reverse=True)):
            if c != d:
                return self.base_priority.compare(c, d)
        return len(s) - len(t)
