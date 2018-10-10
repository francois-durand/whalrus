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
from whalrus.ballots.UtilityBallot import UtilityBallot
from whalrus.ballots.SingleCandidateBallot import SingleCandidateBallot



def make_plurality_ballot(b):
    if not isinstance(b, UtilityBallot):
        b = UtilityBallot(b)

    biggest_val = max(b.values())
    arg_maxs = [c for (c, v) in b.items() if v == biggest_val]

    if len(arg_maxs) > 1:
        raise Exception('Failed to convert ballot to plurality ballot because many candidates have the same score')

    return SingleCandidateBallot(first(arg_maxs), weight=b.weight)
