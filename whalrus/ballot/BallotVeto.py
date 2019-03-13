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
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.priority.Priority import Priority


class BallotVeto(BallotOneName):
    """
    A veto (anti-plurality) ballot.

    >>> ballot = BallotVeto('a', candidates={'a', 'b', 'c'})
    >>> print(ballot)
    a

    >>> ballot = BallotVeto(None, candidates={'a', 'b', 'c'})
    >>> print(ballot)
    None
    """

    # Restrict the ballot
    # ===================

    def _restrict(self, restricted_candidates: set, priority: Priority) -> 'BallotVeto':
        """
        >>> BallotVeto('a', candidates={'a', 'b'}).restrict(candidates={'b'})
        BallotVeto('b', candidates={'b'})
        >>> BallotVeto('a', candidates={'a', 'b', 'c'}).restrict(candidates={'b', 'c'}, priority=Priority.ASCENDING)
        BallotVeto('c', candidates={'b', 'c'})
        """
        return self.__class__(priority.choice(restricted_candidates, reverse=True), candidates=restricted_candidates)

    # First and last candidates
    # =========================

    def first(self, candidates: set=None, **kwargs) -> object:
        """
        >>> BallotVeto('a', candidates={'a', 'b'}).first()
        'b'
        >>> BallotVeto('a', candidates={'a', 'b', 'c'}).first(priority=Priority.ASCENDING)
        'b'
        """
        # noinspection PyUnresolvedReferences
        priority = kwargs.pop('priority', Priority.UNAMBIGUOUS)
        if kwargs:
            raise TypeError("first() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        restricted = self.restrict(candidates=candidates, priority=priority)
        if restricted.candidate is None:
            return None
        top_indifference_class = restricted.candidates_not_in_b
        return priority.choice(top_indifference_class)

    def last(self, candidates: set=None, **kwargs) -> object:
        """
        >>> BallotVeto('a', candidates={'a', 'b', 'c'}).last()
        'a'
        >>> BallotVeto('a', candidates={'a', 'b', 'c'}).last(candidates={'b', 'c'},
        ...                                                  priority=Priority.ASCENDING)
        'c'
        """
        # noinspection PyUnresolvedReferences
        priority = kwargs.pop('priority', Priority.UNAMBIGUOUS)
        if kwargs:
            raise TypeError("last() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        restricted = self.restrict(candidates=candidates, priority=priority)
        return restricted.candidate
