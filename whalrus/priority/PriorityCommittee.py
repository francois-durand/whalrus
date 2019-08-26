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
from functools import cmp_to_key
from whalrus.priority.Priority import Priority
# Ideally, all Union[set, list] in this file should be typing.Collection, but it is only defined in Python >= 3.6.


class PriorityCommittee(Priority):
    """
    A priority setting over committees (= sets of candidates).
    """

    def compare_committees(self, s, t) -> int:
        """
        Compare two committees.

        :param s: a committee.
        :param t: a committee.
        :return: 0 if `s == t`, -1 if the tie is broken in favor of `s` over `t`, 1 otherwise.
        """
        raise NotImplementedError

    def compare(self, c, d) -> int:
        return self.compare_committees({c}, {d})

    def choice_committee(self, x: Union[set, list], reverse: bool = False) -> object:
        """
        Choose an element from a list, set, etc. of committees.

        :param x: the list, set, etc where the committee is to be chosen.
        :param reverse: if False (default), then we choose the "first" or "best" committee in this priority order. If
            True, then we choose the "last" or "worst" committee.
        :return: the chosen committee (or None). When ``x`` is empty, return None. When ``x`` has one element, return
            this element.
        """
        if len(x) == 0:
            return None
        if len(x) == 1:
            return list(x)[0]
        return self._choice_committee(x, reverse=reverse)

    def _choice_committee(self, x: Union[set, list], reverse: bool) -> object:
        """
        Auxiliary function for :meth:`choice`.

        Here, ``x`` is assumed to have at least 2 elements.
        """
        if reverse:
            return max(x, key=cmp_to_key(self.compare_committees))
        else:
            return min(x, key=cmp_to_key(self.compare_committees))

    def sort_committees(self, x: Union[set, list], reverse: bool = False) -> Union[list, None]:
        """
        Sort a list, set, etc. of committees.

        :param x: the list, set, etc.
        :param reverse: if True, we use the reverse priority order.
        :return: a sorted list (or None).

        The original list ``x`` is not modified.
        """
        if len(x) <= 1:
            return list(x)
        return self._sort_committees(x, reverse=reverse)

    def _sort_committees(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        """
        Auxiliary function for :meth:`sort`.

        Here, ``x`` is assumed to have at least 2 elements.
        """
        return sorted(x, key=cmp_to_key(self.compare_committees), reverse=reverse)
