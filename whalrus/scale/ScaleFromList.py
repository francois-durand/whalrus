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

    :param levels: the list of levels, from the worst to the best.
    """

    def __init__(self, levels: list):
        self.levels = list(levels)

    @cached_property
    def as_dict(self):
        return {evaluation: rank for rank, evaluation in enumerate(self.levels)}

    def lt(self, one: object, another: object) -> bool:
        """
        >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
        >>> scale.lt('Medium', 'Excellent')
        True
        """
        return self.as_dict[one] < self.as_dict[another]

    @property
    def low(self) -> object:
        """
        >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
        >>> scale.low
        'Bad'
        """
        return self.levels[0]

    @property
    def high(self) -> object:
        """
        >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
        >>> scale.high
        'Excellent'
        """
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
        """
        >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
        >>> scale.min(['Good', 'Bad', 'Excellent'])
        'Bad'
        """
        return min(iterable, key=lambda level: self.as_dict[level])

    def max(self, iterable: Iterable) -> object:
        """
        >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
        >>> scale.max(['Good', 'Bad', 'Excellent'])
        'Excellent'
        """
        return max(iterable, key=lambda level: self.as_dict[level])

    def sort(self, some_list: list, reverse: bool = False) -> None:
        """
        >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
        >>> some_list = ['Good', 'Bad', 'Excellent']
        >>> scale.sort(some_list)
        >>> some_list
        ['Bad', 'Good', 'Excellent']
        """
        some_list.sort(key=lambda level: self.as_dict[level], reverse=reverse)

    def argsort(self, some_list: list, reverse: bool = False) -> list:
        """
        >>> scale = ScaleFromList(['Bad', 'Medium', 'Good', 'Very good', 'Excellent'])
        >>> scale.argsort(['Good', 'Bad', 'Excellent'])
        [1, 0, 2]
        """
        return sorted(range(len(some_list)), key=lambda i: self.as_dict[some_list[i]], reverse=reverse)
