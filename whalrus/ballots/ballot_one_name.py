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
import logging
from whalrus.ballots.ballot import Ballot
from whalrus.utils.utils import cached_property, NiceSet
from whalrus.priorities.priority import Priority


class BallotOneName(Ballot):
    """
    A ballot in a mono-nominal context (typically plurality or veto).

    Parameters
    ----------
    b : candidate or None
        None stands for abstention.
    candidates : set
        The candidates that were available at the moment when the voter cast her ballot.

    Examples
    --------
        >>> ballot = BallotOneName('a', candidates={'a', 'b', 'c'})
        >>> print(ballot)
        a

        >>> ballot = BallotOneName(None, candidates={'a', 'b', 'c'})
        >>> print(ballot)
        None
    """

    # Core features: ballot and candidates
    # ====================================

    def __init__(self, b: object, candidates: set=None):
        self.candidate = b
        self._input_candidates = candidates
        super().__init__()

    @cached_property
    def candidates(self) -> NiceSet:
        if self._input_candidates is None:
            if self.candidate is None:
                logging.debug('The list of candidates was not explicitly given. Using the empty set instead.')
                return NiceSet()
            else:
                logging.debug('The list of candidates was not explicitly given. Using singleton {%s} instead.'
                              % self.candidate)
                return NiceSet({self.candidate})
        return NiceSet(self._input_candidates)

    @cached_property
    def candidates_in_b(self) -> NiceSet:
        """NiceSet: The candidate that is explicitly mentioned in the ballot.

        This is a singleton with the only candidate contained in the ballot (or an empty set in case of abstention).

        Examples
        --------
            >>> BallotOneName('a', candidates={'a', 'b', 'c'}).candidates_in_b
            {'a'}
            >>> BallotOneName(None, candidates={'a', 'b', 'c'}).candidates_in_b
            {}
        """
        if self.candidate is None:
            return NiceSet()
        else:
            return NiceSet({self.candidate})

    @cached_property
    def candidates_not_in_b(self) -> NiceSet:
        """NiceSet: The candidates that were available at the moment of the vote, but are not explicitly mentioned in
        the ballot.

        Examples
        --------
            >>> BallotOneName('a', candidates={'a', 'b', 'c'}).candidates_not_in_b
            {'b', 'c'}
        """
        return NiceSet(self.candidates - {self.candidate})

    def __eq__(self, other: object) -> bool:
        """Equality test.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            True iff this ballot is equal to `other`. In particular, they must have the same type.

        Examples
        --------
            >>> BallotOneName('a', candidates={'a', 'b', 'c'}) == 'a'
            False

            >>> BallotOneName('a', candidates={'a', 'b', 'c'}) == BallotOneName('a', candidates={'a', 'b'})
            False

            >>> BallotOneName('a', candidates={'a', 'b', 'c'}) == BallotOneName('b', candidates={'a', 'b', 'c'})
            False
        """
        if type(self) != type(other):
            return False
        # noinspection PyUnresolvedReferences
        return self.candidates == other.candidates and self.candidate == other.candidate

    # Representation
    # ==============

    def __repr__(self) -> str:
        return '%s(%s, candidates=%s)' % (self.__class__.__name__, repr(self.candidate), repr(self.candidates))

    def __str__(self) -> str:
        return str(self.candidate)

    # Restrict the ballot
    # ===================

    def restrict(self, candidates: set=None, **kwargs) -> 'BallotOneName':
        """
        Restrict the ballot to less candidates.

        Parameters
        ----------
        candidates : set of candidates
            It can be any set of candidates, not necessarily a subset of ``self.candidates``).
            Default: ``self.candidates``.
        kwargs
            * `priority`: a :class:`Priority`. Default: :attr:`Priority.UNAMBIGUOUS`.

        Returns
        -------
        BallotOneName
            The same ballot, "restricted" to the candidates given.

        Examples
        --------
            >>> BallotOneName('a', candidates={'a', 'b'}).restrict(candidates={'b'})
            BallotOneName('b', candidates={'b'})
            >>> BallotOneName('a', candidates={'a', 'b', 'c'}).restrict(candidates={'b', 'c'},
            ...                                                         priority=Priority.ASCENDING)
            BallotOneName('b', candidates={'b', 'c'})
        """
        # noinspection PyUnresolvedReferences
        priority = kwargs.pop('priority', Priority.UNAMBIGUOUS)
        if kwargs:
            raise TypeError("restrict() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        if candidates is None:
            return self
        if self.candidate in candidates:
            return self.__class__(self.candidate, NiceSet(self.candidates & candidates))
        return self._restrict(restricted_candidates=NiceSet(self.candidates & candidates), priority=priority)

    def _restrict(self, restricted_candidates: NiceSet, priority: Priority) -> 'BallotOneName':
        """
        Auxiliary function of `restrict`.

        Here, it is assumed that `self.candidate` is not in `restricted_candidates`, hence there is really a decision
        to make.

        Parameters
        ----------
        restricted_candidates : NiceSet
            A subset of `self.candidates`.
        priority : Priority

        Returns
        -------
        BallotOneName
            The restricted ballot.
        """
        return self.__class__(priority.choice(restricted_candidates), candidates=restricted_candidates)

    # First and last candidates
    # =========================

    def first(self, candidates: set=None, **kwargs) -> object:
        """
        The first (= most liked) candidate.

        In this parent class, by default, the ballot is considered as a plurality ballot, i.e. the candidate indicated
        is the most liked.

        Parameters
        ----------
        candidates : set of candidates
        kwargs
            * `priority`: a :class:`Priority`. Default: :attr:`Priority.UNAMBIGUOUS`.

        Returns
        -------
        candidate
            The first (= most liked) candidate.

        Examples
        --------
            >>> BallotOneName('a', candidates={'a', 'b', 'c'}).first()
            'a'
            >>> BallotOneName('a', candidates={'a', 'b', 'c'}).first(candidates={'b', 'c'},
            ...                                                      priority=Priority.ASCENDING)
            'b'
        """
        # noinspection PyUnresolvedReferences
        priority = kwargs.pop('priority', Priority.UNAMBIGUOUS)
        if kwargs:
            raise TypeError("first() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        restricted = self.restrict(candidates=candidates, priority=priority)
        return restricted.candidate

    def last(self, candidates: set=None, **kwargs) -> object:
        """
        The last (= most disliked) candidate.

        In this parent class, by default, the ballot is considered as a plurality ballot, i.e. the candidate indicated
        is the most liked.

        Parameters
        ----------
        candidates : set of candidates
        kwargs
            * `priority`: a :class:`Priority`. Default: :attr:`Priority.UNAMBIGUOUS`.

        Returns
        -------
        candidate
            The last (= most disliked) candidate.

        Examples
        --------
            >>> BallotOneName('a', candidates={'a', 'b'}).last()
            'b'
            >>> BallotOneName('a', candidates={'a', 'b', 'c'}).last(priority=Priority.ASCENDING)
            'c'
        """
        # noinspection PyUnresolvedReferences
        priority = kwargs.pop('priority', Priority.UNAMBIGUOUS)
        if kwargs:
            raise TypeError("last() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        restricted = self.restrict(candidates=candidates, priority=priority)
        if restricted.candidate is None:
            return None
        bottom_indifference_class = restricted.candidates_not_in_b
        return priority.choice(bottom_indifference_class, reverse=True)
