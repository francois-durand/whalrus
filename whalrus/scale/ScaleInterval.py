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


class ScaleInterval(Scale):
    """
    A scale given by an interval of floats.

    :param low: lowest float.
    :param high: highest float.

    >>> ScaleInterval(low=0., high=10.)
    ScaleInterval(low=0.0, high=10.0)
    """

    def __init__(self, low: float = 0., high: float = 1.):
        self.low = low
        self.high = high

    def __repr__(self):
        return 'ScaleInterval(low=%s, high=%s)' % (self.low, self.high)
