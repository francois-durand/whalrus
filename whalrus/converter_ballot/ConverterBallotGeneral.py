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
from pyparsing import ParseException
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.ballot.Ballot import Ballot
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.priority.Priority import Priority


# noinspection PyUnresolvedReferences
class ConverterBallotGeneral(ConverterBallot):
    """
    General ballot converter.

    :param plurality_priority: option passed to :meth:`BallotPlurality.restrict` when restricting the ballot if,
        once converted, it is a :class:`BallotPlurality`.
    :param veto_priority: option passed to :meth:`BallotVeto.restrict` when restricting the ballot if, once converted,
        if is a :class:`BallotVeto`.
    :param one_name_priority: option passed to :meth:`BallotOneName.restrict` when restricting the ballot if, once
        converted, it is a :class:`BallotOneName` (but not a :class:`BallotPlurality` or :class:`BallotVeto`).

    This is a default general converter. It tries to infer the type of input and converts it to an object of the
    relevant subclass of :class:`Ballot`.

    Typical usage:

    >>> converter = ConverterBallotGeneral()
    >>> converter({'a': 10, 'b': 7, 'c': 0})
    BallotLevels({'a': 10, 'b': 7, 'c': 0}, candidates={'a', 'b', 'c'}, scale=Scale())
    >>> converter([{'a', 'b'}, {'c'}])
    BallotOrder([{'a', 'b'}, 'c'], candidates={'a', 'b', 'c'})
    >>> converter('a ~ b > c')
    BallotOrder([{'a', 'b'}, 'c'], candidates={'a', 'b', 'c'})
    >>> converter('Alice')
    BallotOneName('Alice', candidates={'Alice'})

    It is also possible to "restrict" the set of candidates on-the-fly:

    >>> converter = ConverterBallotGeneral()
    >>> converter('a ~ b > c', candidates={'b', 'c'})
    BallotOrder(['b', 'c'], candidates={'b', 'c'})
    >>> converter({'a': 10, 'b': 7, 'c': 0}, candidates={'b', 'c'})
    BallotLevels({'b': 7, 'c': 0}, candidates={'b', 'c'}, scale=Scale())

    Cf. :meth:`Ballot.restrict` for more information.

    Use options for the restrictions:

    >>> converter = ConverterBallotGeneral(one_name_priority=Priority.ASCENDING,
    ...                                    plurality_priority=Priority.ASCENDING,
    ...                                    veto_priority=Priority.ASCENDING)
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'}), candidates={'b', 'c'})
    BallotOneName('b', candidates={'b', 'c'})
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'}), candidates={'b', 'c'})
    BallotPlurality('b', candidates={'b', 'c'})
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'}), candidates={'b', 'c'})
    BallotVeto('c', candidates={'b', 'c'})
    """

    def __init__(self,
                 plurality_priority: Priority = Priority.UNAMBIGUOUS,
                 veto_priority: Priority=Priority.UNAMBIGUOUS,
                 one_name_priority: Priority=Priority.UNAMBIGUOUS):
        self.plurality_priority = plurality_priority
        self.veto_priority = veto_priority
        self.one_name_priority = one_name_priority

    def __call__(self, x: object, candidates: set=None) -> Ballot:
        # If it is a ballot, deal with the restriction to the candidates.
        if isinstance(x, Ballot):
            if candidates is None:
                return x
            if isinstance(x, BallotOrder):
                return x.restrict(candidates)
            if isinstance(x, BallotPlurality):
                return x.restrict(candidates=candidates, priority=self.plurality_priority)
            if isinstance(x, BallotVeto):
                return x.restrict(candidates=candidates, priority=self.veto_priority)
            if isinstance(x, BallotOneName):
                return x.restrict(candidates=candidates, priority=self.one_name_priority)
            raise NotImplementedError('Unable to restrict the candidates for ballot of class %s.' % x.__class__)
        # If it is not a ballot, convert to ballot and call the method again.
        if isinstance(x, dict):
            return self(BallotLevels(x), candidates)
        try:
            ballot_order = BallotOrder(x)
            if len(ballot_order) == 1:
                return self(BallotOneName(x), candidates)
            else:
                return self(ballot_order, candidates)
        except (TypeError, ParseException):
            pass
        return self(BallotOneName(x), candidates)
