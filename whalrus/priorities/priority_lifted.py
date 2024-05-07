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
from whalrus.priorities.priority import Priority


class PriorityLifted(Priority):
    """
    A priority setting over committees (= sets of candidates), computed from lifting a priority on candidates.

    For some examples, cf. :class:`PriorityLiftedLeximax`.
    """

    def __init__(self, name: str, base_priority: Priority = Priority.UNAMBIGUOUS):
        self.base_priority = base_priority
        super().__init__(name=name)

    def compare_committees(self, s, t) -> int:
        raise NotImplementedError

    def compare(self, c, d) -> int:
        return self.base_priority.compare(c, d)

    def choose(self, x: Union[set, list], reverse: bool = False) -> object:
        return self.base_priority.choice(x, reverse)

    def sort(self, x: Union[set, list], reverse: bool = False) -> Union[list, None]:
        return self.base_priority.sort(x, reverse)

    def sort_pairs_rp(self, x: Union[set, list], reverse: bool = False) -> Union[list, None]:
        return self.base_priority.sort_pairs_rp(x, reverse)
