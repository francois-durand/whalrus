
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
from typing import Dict, Any
from whalrus.ballots.Ballot import Ballot
from whalrus.utils.check_types import type_set
from whalrus.ballots.SingleCandidateBallot import SingleCandidateBallot
from toolz import first



class UtilityBallot(Ballot):
    """
    Class used to create a ballot where each item has a utility

    >>> b1  = UtilityBallot({'jean':23,'pie':12,'doublas':42})
    >>> b2 = UtilityBallot(['jean','pie','doug'])
    >>> b3 = UtilityBallot('jean')

    You can also add a weight to your ballot
    >>> b4 = UtilityBallot(['jean','pie','doug'],weight=2.0)
    """

    def __init__(self, b,weight=None):
        self.weight = weight

        if type(b) == dict and type_set(b.values()) <= {int,float}:
            super().__init__(b)

        elif type(b) in [list, tuple, set] and type_set(b) <= {str}: # changer en iterable
            super().__init__({x: i for i, x in enumerate(reversed(list(b)))})

        elif type(b) == str:
            super().__init__({b:0})
        else:
            raise TypeError('expecting dict,list,tuple or set')




if __name__ ==  '__main__':
    import doctest
    doctest.testmod()
