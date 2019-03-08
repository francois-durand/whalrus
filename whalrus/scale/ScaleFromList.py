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
import numbers
from whalrus.scale.Scale import Scale
from whalrus.utils.Utils import cached_property
from typing import Iterable


class ScaleFromList(Scale):
    """
    Scale derived from a list.

    :param levels: list of levels, from the worst to the best.

    >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
    >>> scale
    ScaleFromList(levels=['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
    >>> scale.lt('Medium', 'Excellent')
    True
    >>> scale.gt('Medium', 'Excellent')
    False
    >>> scale.low
    'Bad'
    >>> scale.high
    'Excellent'
    """

    def __init__(self, levels: list):
        self.levels = list(levels)
        self.as_dict = {evaluation: rank for rank, evaluation in enumerate(levels)}

    def lt(self, one: object, another: object) -> bool:
        return self.as_dict[one] < self.as_dict[another]

    @property
    def low(self) -> object:
        return self.levels[0]

    @property
    def high(self) -> object:
        return self.levels[-1]

    @property
    def is_bounded(self) -> bool:
        return True

    @cached_property
    def is_numeric(self) -> bool:
        return all([isinstance(v, numbers.Number) for v in self.levels])

    def __repr__(self):
        return 'ScaleFromList(levels=%s)' % self.levels

    # Min, max and sort
    # -----------------

    def min(self, iterable: Iterable) -> object:
        return min(iterable, key=lambda level: self.as_dict[level])

    def max(self, iterable: Iterable) -> object:
        return max(iterable, key=lambda level: self.as_dict[level])

    def sort(self, some_list: list) -> None:
        some_list.sort(key=lambda level: self.as_dict[level])

    def argsort(self, some_list: list) -> list:
        return sorted(range(len(some_list)), key=lambda i: self.as_dict[some_list[i]])
