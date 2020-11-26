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
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.utils.Utils import set_to_str


class ScaleFromSet(ScaleFromList):
    # noinspection PyUnresolvedReferences
    """
    Scale derived from a set.

    :param levels: a set of comparable objects. It is recommended that they are also hashable.

    Typical usage:

    >>> scale = ScaleFromSet({-1, 0, 2})

    A more complex example:

    >>> class Appreciation:
    ...     VALUES = {'Excellent': 2, 'Good': 1, 'Medium': 0}
    ...     def __init__(self, x):
    ...         self.x = x
    ...     def __repr__(self):
    ...         return 'Appreciation(%r)' % self.x
    ...     def __hash__(self):
    ...         return hash(self.x)
    ...     def __lt__(self, other):
    ...         return Appreciation.VALUES[self.x] < Appreciation.VALUES[other.x]
    >>> scale = ScaleFromSet({Appreciation('Excellent'), Appreciation('Good'),
    ...                      Appreciation('Medium')})
    >>> scale.lt(Appreciation('Medium'), Appreciation('Good'))
    True
    >>> scale.low
    Appreciation('Medium')
    >>> scale.high
    Appreciation('Excellent')
    """

    def __init__(self, levels: set):
        super().__init__(sorted(levels))

    # noinspection PyMethodMayBeStatic
    def lt(self, one: object, another: object) -> bool:
        """
        >>> scale = ScaleFromSet({-1, 0, 2})
        >>> scale.lt(0, 2)
        True
        """
        return one < another

    def __repr__(self):
        return 'ScaleFromSet(levels=%s)' % set_to_str(set(self.levels))
