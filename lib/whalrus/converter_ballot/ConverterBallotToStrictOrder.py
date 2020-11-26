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
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.priority.Priority import Priority
from itertools import chain


class ConverterBallotToStrictOrder(ConverterBallot):
    """
    Default converter to a strictly ordered ballot.

    :param priority: the :class:`Priority` used to break ties. Default: :attr:`Priority.UNAMBIGUOUS`.

    This is a default converter to a strictly ordered ballot (cf. :attr:`BallotOrder.is_strict`). It tries to infer
    the type of input and converts it to a :class:`BallotOrder` (possibly a ballot of a subclass, such as
    :class:`BallotLevels`), ensuring that the represented order is strict.

    >>> converter = ConverterBallotToStrictOrder(priority=Priority.ASCENDING)
    >>> converter('a > b ~ c')
    BallotOrder(['a', 'b', 'c'], candidates={'a', 'b', 'c'})
    >>> converter(['a', {'b', 'c'}])
    BallotOrder(['a', 'b', 'c'], candidates={'a', 'b', 'c'})
    >>> converter({'a': 10, 'b': 7, 'c': 0})
    BallotLevels({'a': 10, 'b': 7, 'c': 0}, candidates={'a', 'b', 'c'}, scale=Scale())
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['a', 'b', 'c'], candidates={'a', 'b', 'c'})
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['a', 'b', 'c'], candidates={'a', 'b', 'c'})
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['b', 'c', 'a'], candidates={'a', 'b', 'c'})
    """

    def __init__(self, priority: Priority = Priority.UNAMBIGUOUS):
        self.priority = priority

    def __call__(self, x: object, candidates: set = None) -> BallotOrder:
        x = ConverterBallotToOrder()(x, candidates=candidates)
        if x.is_strict:
            return x
        else:
            return BallotOrder(list(chain(*[
                self.priority.sort(indifference_class) for indifference_class in x.as_weak_order
            ])))
