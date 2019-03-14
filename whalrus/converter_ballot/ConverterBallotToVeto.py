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
from whalrus.ballot.Ballot import Ballot
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.priority.Priority import Priority


class ConverterBallotToVeto(ConverterBallot):
    """
    Default converter to a :class:`BallotVeto`.

    :param priority: serves as a default value for the other parameters if they are not explicitly mentioned. Default:
        :attr:`Priority.UNAMBIGUOUS`.
    :param order_priority: option passed to :meth:`BallotOrder.last`. Default: ``priority``.
    :param plurality_priority: option passed to :meth:`BallotPlurality.last`. Default: ``priority``.
    :param veto_priority: option passed to :meth:`BallotVeto.last`. Default: ``priority``.
    :param one_name_priority: option passed to :meth:`BallotOneName.last`. Default: ``priority``.

    Typical usages:

    >>> converter = ConverterBallotToVeto()
    >>> converter(BallotOneName('a', candidates={'a', 'b'}))
    BallotVeto('a', candidates={'a', 'b'})
    >>> converter(BallotPlurality('a', candidates={'a', 'b'}))
    BallotVeto('b', candidates={'a', 'b'})
    >>> converter({'a': 10, 'b': 7, 'c':0})
    BallotVeto('c', candidates={'a', 'b', 'c'})
    >>> converter('a ~ b > c')
    BallotVeto('c', candidates={'a', 'b', 'c'})
    >>> converter([{'a', 'b'}, 'c'])
    BallotVeto('c', candidates={'a', 'b', 'c'})

    Use options for the restrictions:

    >>> converter = ConverterBallotToVeto(priority=Priority.ASCENDING)
    >>> converter('a > b ~ c')
    BallotVeto('c', candidates={'a', 'b', 'c'})
    """

    def __init__(self,
                 priority: Priority = Priority.UNAMBIGUOUS,
                 order_priority: Priority = None,
                 plurality_priority: Priority = None,
                 veto_priority: Priority = None,
                 one_name_priority: Priority = None):
        # Default parameters
        if order_priority is None:
            order_priority = priority
        if plurality_priority is None:
            plurality_priority = priority
        if veto_priority is None:
            veto_priority = priority
        if one_name_priority is None:
            one_name_priority = priority
        # Parameters
        self.order_priority = order_priority
        self.plurality_priority = plurality_priority
        self.veto_priority = veto_priority
        self.one_name_priority = one_name_priority

    def __call__(self, x: object, candidates: set = None) -> BallotVeto:
        x = ConverterBallotGeneral()(x, candidates=None)
        if isinstance(x, BallotPlurality):
            last = x.last(candidates=candidates, priority=self.plurality_priority)
            if candidates is None:
                candidates = x.candidates
            else:
                candidates = x.candidates & candidates
            return BallotVeto(last, candidates=candidates)
        if isinstance(x, BallotVeto):
            return x.restrict(candidates=candidates, priority=self.veto_priority)
        if isinstance(x, BallotOneName):
            x = BallotVeto(x.candidate, candidates=x.candidates)
            return x.restrict(candidates=candidates, priority=self.one_name_priority)
        if isinstance(x, BallotOrder):
            x = x.restrict(candidates=candidates)
            return BallotVeto(x.last(priority=self.order_priority), candidates=x.candidates)
        if isinstance(x, Ballot):
            x = ConverterBallotGeneral()(x, candidates=candidates)
            return BallotVeto(x.last(), candidates=x.candidates)
