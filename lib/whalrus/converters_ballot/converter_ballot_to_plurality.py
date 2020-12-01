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
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.ballots.ballot import Ballot
from whalrus.ballots.ballot_plurality import BallotPlurality
from whalrus.ballots.ballot_veto import BallotVeto
from whalrus.ballots.ballot_one_name import BallotOneName
from whalrus.ballots.ballot_order import BallotOrder
from whalrus.priorities.priority import Priority


class ConverterBallotToPlurality(ConverterBallot):
    """
    Default converter to a :class:`BallotPlurality`.

    Parameters
    ----------
    priority : Priority
        Serves as a default value for the other parameters if they are not explicitly mentioned. Default:
        :attr:`Priority.UNAMBIGUOUS`.
    order_priority : Priority
        Option passed to :meth:`BallotOrder.first`. Default: ``priority``.
    plurality_priority : Priority
        Option passed to :meth:`BallotPlurality.first`. Default: ``priority``.
    veto_priority : Priority
        Option passed to :meth:`BallotVeto.first`. Default: ``priority``.
    one_name_priority : Priority
        Option passed to :meth:`BallotOneName.first`. Default: ``priority``.

    Examples
    --------
    Typical usages:

        >>> converter = ConverterBallotToPlurality()
        >>> converter(BallotOneName('a', candidates={'a', 'b'}))
        BallotPlurality('a', candidates={'a', 'b'})
        >>> converter(BallotVeto('a', candidates={'a', 'b'}))
        BallotPlurality('b', candidates={'a', 'b'})
        >>> converter({'a': 10, 'b': 7, 'c':0})
        BallotPlurality('a', candidates={'a', 'b', 'c'})
        >>> converter('a > b ~ c')
        BallotPlurality('a', candidates={'a', 'b', 'c'})
        >>> converter(['a', {'b', 'c'}])
        BallotPlurality('a', candidates={'a', 'b', 'c'})

    Use options for the restrictions:

        >>> converter = ConverterBallotToPlurality(priority=Priority.ASCENDING)
        >>> converter('a ~ b > c')
        BallotPlurality('a', candidates={'a', 'b', 'c'})

    Misc:

        >>> ballot = BallotVeto('a', candidates={'a', 'b', 'c'})
        >>> converter = ConverterBallotToPlurality()
        >>> converter(ballot, candidates={'a', 'b', 'd'})
        BallotPlurality('b', candidates={'a', 'b'})
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

    def __call__(self, x: object, candidates: set = None) -> BallotPlurality:
        x = ConverterBallotGeneral()(x, candidates=None)
        if isinstance(x, BallotPlurality):
            return x.restrict(candidates=candidates, priority=self.plurality_priority)
        if isinstance(x, BallotVeto):
            first = x.first(candidates=candidates, priority=self.veto_priority)
            if candidates is None:
                candidates = x.candidates
            else:
                candidates = x.candidates & candidates
            return BallotPlurality(first, candidates=candidates)
        if isinstance(x, BallotOneName):
            x = BallotPlurality(x.candidate, candidates=x.candidates)
            return x.restrict(candidates=candidates, priority=self.one_name_priority)
        if isinstance(x, BallotOrder):
            x = x.restrict(candidates=candidates)
            return BallotPlurality(x.first(priority=self.order_priority), candidates=x.candidates)
        if isinstance(x, Ballot):
            x = ConverterBallotGeneral()(x, candidates=candidates)
            return BallotPlurality(x.first(), candidates=x.candidates)
