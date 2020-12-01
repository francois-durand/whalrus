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
from typing import Iterable
from whalrus.ballots.ballot import Ballot
from whalrus.utils.utils import parse_weak_order, cached_property, set_to_list, NiceSet
from whalrus.priorities.priority import Priority


class BallotOrder(Ballot):
    """
    Ballot with an ordering.

    Parameters
    ----------
    b : object
        The ballot. Cf. examples below for the accepted formats.
    candidates : set
        The candidates that were available at the moment when the voter cast her ballot. Default:
        candidates that are explicitly mentioned in the ballot :attr:`b`.

    Examples
    --------
    Most general syntax:

        >>> ballot = BallotOrder([{'a', 'b'}, {'c'}], candidates={'a', 'b', 'c', 'd', 'e'})
        >>> ballot
        BallotOrder([{'a', 'b'}, 'c'], candidates={'a', 'b', 'c', 'd', 'e'})
        >>> print(ballot)
        a ~ b > c (unordered: d, e)

    In the example above, candidates `a` and `b` are equally liked, and they are liked better than `c`. Candidates
    `d` and `e` were available when the voter cast her ballot, but she chose not to include them in her preference
    order.

    Other examples of inputs:

        >>> BallotOrder('a ~ b > c')
        BallotOrder([{'a', 'b'}, 'c'], candidates={'a', 'b', 'c'})
        >>> BallotOrder({'a': 10, 'b': 10, 'c': 7})
        BallotOrder([{'a', 'b'}, 'c'], candidates={'a', 'b', 'c'})

    The ballot has a set-like behavior in the sense that it implements ``__len__`` and ``__contains__``:

        >>> ballot = BallotOrder('a ~ b > c', candidates={'a', 'b', 'c', 'd', 'e'})
        >>> len(ballot)
        3
        >>> 'd' in ballot
        False

    If the order is strict, then the ballot is also iterable:

        >>> ballot = BallotOrder('a > b > c')
        >>> for candidate in ballot:
        ...     print(candidate)
        a
        b
        c
    """

    # Core features: ballot and candidates
    # ====================================

    def __init__(self, b: object, candidates: set=None):
        self._internal_representation = None
        self._parse(b)
        self._input_candidates = candidates
        super().__init__()

    def _parse(self, b: object) -> None:
        """
        Assign `self._internal_representation`.

        The form of `self._internal_representation` may depend on the subclass. For the mother class `BallotOrder`,
        it is of the form [{'a', 'b'}, {'c'}], meaning a ~ b > c. It is used directly for self.as_weak_order.

        Parameters
        ----------
        b : object
            The ballot in a loose input format (cf. documentation of the class and unit tests).
        """
        if isinstance(b, tuple):
            b = list(b)
        if isinstance(b, list):
            self._internal_representation = [NiceSet(s) if isinstance(s, set) else NiceSet({s}) for s in b]
        elif isinstance(b, dict):
            self._internal_representation = [NiceSet({k for k in b.keys() if b[k] == v})
                                             for v in sorted(set(b.values()), reverse=True)]
        elif isinstance(b, str):
            self._internal_representation = parse_weak_order(b)
        else:
            raise TypeError('Cannot interpret as an order: %r.' % b)

    @cached_property
    def as_weak_order(self) -> list:
        """list: Weak order format.

        A list of sets. For example, ``[{'a', 'b'}, {'c'}]`` means that `a` and `b` are equally liked, and they are
        liked better than `c`.

        Examples
        --------
            >>> BallotOrder('a ~ b > c', candidates={'a', 'b', 'c', 'd', 'e'}).as_weak_order
            [{'a', 'b'}, {'c'}]
        """
        return self._internal_representation

    @cached_property
    def candidates_in_b(self) -> NiceSet:
        """NiceSet: the candidates that are explicitly mentioned in the ballot.

        Examples
        --------
            >>> BallotOrder('a ~ b > c', candidates={'a', 'b', 'c', 'd', 'e'}).candidates_in_b
            {'a', 'b', 'c'}
        """
        return NiceSet(c for indifference_class in self.as_weak_order for c in indifference_class)

    @cached_property
    def candidates(self) -> NiceSet:
        """NiceSet: the candidates.

        If the set was not explicitly given, the candidates are inferred from the ballot.

        Examples
        --------
            >>> BallotOrder('a ~ b > c', candidates={'a', 'b', 'c', 'd', 'e'}).candidates
            {'a', 'b', 'c', 'd', 'e'}
            >>> BallotOrder('a ~ b > c').candidates
            {'a', 'b', 'c'}
        """
        if self._input_candidates is None:
            return self.candidates_in_b
        return NiceSet(self._input_candidates)

    # Misc
    # ====

    @cached_property
    def candidates_not_in_b(self) -> NiceSet:
        """NiceSet: the candidates that were available at the moment of the vote, but are not explicitly mentioned in
        the ballot.

        Examples
        --------
            >>> BallotOrder('a ~ b > c', candidates={'a', 'b', 'c', 'd', 'e'}).candidates_not_in_b
            {'d', 'e'}
        """
        return NiceSet(self.candidates - self.candidates_in_b)

    def __len__(self) -> int:
        """int: Number of candidates explicitly mentioned in the ballot.

        It is the length of self.candidates_in_b.

        Examples
        --------
            >>> len(BallotOrder('a ~ b > c', candidates={'a', 'b', 'c', 'd', 'e'}))
            3
        """
        return len(self.candidates_in_b)

    def __contains__(self, item: object) -> bool:
        """
        Whether a candidate is explicitly mentioned in the ballot.

        Parameters
        ----------
        item : candidate

        Returns
        -------
        bool
            True iff the candidate is explicitly mentioned in the ballot.

        Examples
        --------
            >>> 'd' in BallotOrder('a ~ b > c', candidates={'a', 'b', 'c', 'd', 'e'})
            False
        """
        return item in self.candidates_in_b

    def __eq__(self, other: object) -> bool:
        """Equality test.

        Parameters
        ----------
        other : object

        Returns
        -------
        bool
            True if the two objects are equal. In particular, they must have the same type.

        Examples
        --------
            >>> ballot = BallotOrder('a > b > c')
            >>> ballot == 'a > b > c'
            False
            >>> ballot == BallotOrder('a > b > c', candidates={'a', 'b', 'c', 'd'})
            False
        """
        if type(self) != type(other):
            return False
        # noinspection PyProtectedMember,PyUnresolvedReferences
        return self.candidates == other.candidates and self._internal_representation == other._internal_representation

    # Representation
    # ==============

    def __repr__(self) -> str:
        return 'BallotOrder(%s, candidates=%s)' % (
            '[' + ', '.join([
                repr(indifference_class) if len(indifference_class) > 1 else repr(list(indifference_class)[0])
                for indifference_class in self.as_weak_order
            ]) + ']',
            repr(self.candidates)
        )

    def __str__(self) -> str:
        result = []
        if self.candidates_in_b:
            result.append(' > '.join([
                ' ~ '.join([str(candidate) for candidate in set_to_list(indifference_class)])
                for indifference_class in self.as_weak_order
            ]))
        if self.candidates_not_in_b:
            result.append(
                '(unordered: '
                + ', '.join([str(candidate) for candidate in set_to_list(self.candidates_not_in_b)])
                + ')'
            )
        return ' '.join(result)

    # Restrict the ballot
    # ===================

    def restrict(self, candidates: set=None, **kwargs) -> 'BallotOrder':
        """
        Restrict the ballot to less candidates.

        Parameters
        ----------
        candidates : set of candidates
            It can be any set of candidates, not necessarily a subset of ``self.candidates``).
            Default: ``self.candidates``.
        kwargs
            Some options (depending on the subclass).

        Returns
        -------
        BallotOrder
            The same ballot, "restricted" to the candidates given.

        Examples
        --------
        Typical usage:

            >>> ballot = BallotOrder('a ~ b > c')
            >>> ballot
            BallotOrder([{'a', 'b'}, 'c'], candidates={'a', 'b', 'c'})
            >>> ballot.restrict(candidates={'b', 'c'})
            BallotOrder(['b', 'c'], candidates={'b', 'c'})

        More general usage:

            >>> ballot.restrict(candidates={'b', 'c', 'd'})
            BallotOrder(['b', 'c'], candidates={'b', 'c'})

        In the last example above, note that `d` is not in the candidates of the restricted ballot, as she was not
        available at the moment when the voter cast her ballot.
        """
        if kwargs:
            raise TypeError("restrict() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        if candidates is None:
            return self
        weak = [indifference_class & candidates for indifference_class in self.as_weak_order]
        weak = [indifference_class for indifference_class in weak if indifference_class]
        return BallotOrder(weak, candidates=self.candidates & candidates)

    # First and last candidates
    # =========================

    def first(self, candidates: set=None, **kwargs) -> object:
        """
        The first (= most liked) candidate.

        Parameters
        ----------
        candidates : set of candidates
            It can be any set of candidates, not necessarily a subset of ``self.candidates``.
            Default: ``self.candidates``.
        kwargs
            * `priority`: a :class:`Priority`. Default: :attr:`Priority.UNAMBIGUOUS`.
            * `include_unordered`: a boolean. If True (default), then unordered candidates are considered present but
              below the others.

        Returns
        -------
        candidate
            The first (= most liked) candidate, chosen in the intersection of ``self.candidates`` and the argument
            ``candidates``. Can return None for an "abstention".

        Examples
        --------
            >>> print(BallotOrder('a ~ b').first(priority=Priority.ASCENDING))
            a
            >>> print(BallotOrder('a > b', candidates={'a', 'b', 'c'}).first(candidates={'c'}))
            c
            >>> print(BallotOrder('a > b', candidates={'a', 'b', 'c'}).first(candidates={'c'},
            ...                                                              include_unordered=False))
            None
        """
        priority = kwargs.pop('priority', Priority.UNAMBIGUOUS)
        include_unordered = kwargs.pop('include_unordered', True)
        if kwargs:
            raise TypeError("first() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        # Do the job
        restricted = self.restrict(candidates=candidates)
        if len(restricted.as_weak_order) == 0:
            if include_unordered:
                top_indifference_class = restricted.candidates_not_in_b
            else:
                top_indifference_class = {}
        else:
            top_indifference_class = restricted.as_weak_order[0]
        return priority.choice(top_indifference_class)

    def last(self, candidates: set=None, **kwargs) -> object:
        """
        The last (= most disliked) candidate.

        Parameters
        ----------
        candidates : set of candidates
            It can be any set of candidates, not necessarily a subset of ``self.candidates``.
            Default is ``self.candidates``.
        kwargs
            * `priority`: a :class:`Priority` object. Default: :attr:`Priority.UNAMBIGUOUS`.
            * `include_unordered`: a boolean. If True (default), then unordered candidates are considered present but
              below the others.

        Returns
        -------
        candidate
            The last (= most disliked) candidate, chosen in the intersection of ``self.candidates`` and the
            argument ``candidates``. Can return None for an "abstention".

        Examples
        --------
            >>> print(BallotOrder('a ~ b').last(priority=Priority.ASCENDING))
            b
            >>> print(BallotOrder('a > b', candidates={'a', 'b', 'c'}).last())
            c
            >>> print(BallotOrder('a > b', candidates={'a', 'b', 'c'}).last(include_unordered=False))
            b
            >>> ballot = BallotOrder('a > b', candidates={'a', 'b', 'c', 'd'})
            >>> print(ballot.last(candidates={'c', 'd'}, include_unordered=False))
            None
        """
        # noinspection PyUnresolvedReferences
        priority = kwargs.pop('priority', Priority.UNAMBIGUOUS)
        include_unordered = kwargs.pop('include_unordered', True)
        if kwargs:
            raise TypeError("last() got an unexpected keyword argument %r" % list(kwargs.keys())[0])
        # Do the job
        restricted = self.restrict(candidates=candidates)
        if include_unordered and restricted.candidates_not_in_b:
            bottom_indifference_class = restricted.candidates_not_in_b
        elif len(restricted.as_weak_order) == 0:
            bottom_indifference_class = {}
        else:
            bottom_indifference_class = restricted.as_weak_order[-1]
        return priority.choice(bottom_indifference_class, reverse=True)

    # Strict order features (if relevant)
    # ===================================

    @cached_property
    def is_strict(self) -> bool:
        """bool: Whether the ballot is a strict order or not.

        True if the order is strict, i.e. if each indifference class contains one element. There can be some unordered
        candidates.

        Examples
        --------
            >>> BallotOrder('a > b > c').is_strict
            True
            >>> BallotOrder('a > b > c', candidates={'a', 'b', 'c', 'd', 'e'}).is_strict
            True
            >>> BallotOrder('a ~ b > c').is_strict
            False
        """
        return all([len(s) == 1 for s in self.as_weak_order])

    def _check_strict(self) -> None:
        """
        Test strictness and raise an exception if not strict.

        Raises
        ------
        ValueError
            If the order is not strict.
        """
        if not self.is_strict:
            raise ValueError('This order is not strict: %s.' % self.as_weak_order)

    @cached_property
    def as_strict_order(self) -> list:
        """list : Strict order format.

        It is a list of candidates. For example, ``['a', 'b', 'c']`` means that `a` is preferred to `b`, who is
        preferred to `c`.

        Raises
        ------
        ValueError
            If the ballot is not a strict order.

        Examples
        --------
            >>> BallotOrder('a > b > c').as_strict_order
            ['a', 'b', 'c']
        """
        self._check_strict()
        return [list(indifference_class)[0] for indifference_class in self.as_weak_order]

    def __iter__(self) -> Iterable:
        """Iterate over the candidates of a strict order.

        Returns
        -------
        Iterable
            Over the candidates, from most liked to least liked.

        Examples
        --------
            >>> for candidate in BallotOrder('a > b > c'):
            ...     print(candidate)
            a
            b
            c
        """
        self._check_strict()
        return iter(self.as_strict_order)
