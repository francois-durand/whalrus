
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


class UtilityBallot(Ballot):
    def __init__(self, b,weight=None):
        """
        Class used to create a ballot where each item has a utility

        >>> myBallot  = UtilityBallot({'jean':23,'pie':12,'doublas':42})
        >>> myBallot2 = UtilityBallot(['jean','pie','doug'])
        """
        self.weight = weight

        if type(b) == dict and type_set(b.values()) <= [int,float]:
            super().__init__(b)

        elif type(b) in [list, tuple, set] and type_set(b) <= [str]: # changer en iterable
            super().__init__({x: i for i, x in enumerate(reversed(list(b)))})

        elif type(b) == str:
            super().__init__({b:0})
        else:
            raise TypeError('expecting dict,list,tuple or set')


    def to_plurality_ballot(self):

        smallest_val = min(self.values())
        arg_mins     = [c for c,v in self.items() if v==smallest_val]

        if len(arg_mins) > 1:
            raise 'Failed to convert ballot to plurality ballot because many candidates have the same score'

        return SingleCandidateBallot( first(arg_mins) , weight=self.weight )
