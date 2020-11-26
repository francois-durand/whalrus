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
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOrder import BallotOrder


class ConverterBallotToOrder(ConverterBallot):
    """
    Default converter to a :class:`BallotOrder`.

    This is a default converter to a :class:`BallotOrder`. It tries to infer the type of input and converts it to
    an ordered ballot (possibly a ballot of a subclass, such as :class:`BallotLevels`).

    >>> converter = ConverterBallotToOrder()
    >>> converter('a > b ~ c')
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> converter(['a', {'b', 'c'}])
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> converter({'a': 10, 'b': 7, 'c': 0})
    BallotLevels({'a': 10, 'b': 7, 'c': 0}, candidates={'a', 'b', 'c'}, scale=Scale())
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'}))
    BallotOrder([{'b', 'c'}, 'a'], candidates={'a', 'b', 'c'})
    """

    def __call__(self, x: object, candidates: set = None) -> BallotOrder:
        x = ConverterBallotGeneral()(x, candidates=None)
        if isinstance(x, BallotOrder):
            return x.restrict(candidates=candidates)
        if isinstance(x, BallotVeto):
            return BallotOrder([x.candidates_not_in_b, {x.last()}]).restrict(candidates=candidates)
        if isinstance(x, BallotOneName):
            return BallotOrder([{x.first()}, x.candidates_not_in_b]).restrict(candidates=candidates)
        raise NotImplementedError
