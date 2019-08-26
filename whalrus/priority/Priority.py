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
import random
from typing import Union
from functools import cmp_to_key
# Ideally, all Union[set, list] in this file should be typing.Collection, but it is only defined in Python >= 3.6.


class Priority:
    """
    A priority setting, i.e. a policy to break ties and indifference classes.

    In all generality, a Priority object is supposed to compare committees, i.e. sets of candidates. But it may
    not be able to compare any two committees. In particular, some Priority objects, such as Priority.ASCENDING, can
    only compare committees of size 1, i.e. candidates, which is generally sufficient to break ties in a single-winner
    voting rule. Cf. :meth:`compare_committees` and :meth:`compare`.

    :param name: the name of this priority setting.

    Typical usage:

    >>> priority = Priority.ASCENDING
    >>> priority.choose({'c', 'a', 'b'})
    'a'
    >>> priority.sort({'c', 'a', 'b'})
    ['a', 'b', 'c']

    :cvar UNAMBIGUOUS: shortcut for :class:`PriorityUnambiguous`.
    :cvar ABSTAIN: shortcut for :class:`PriorityAbstain`.
    :cvar RANDOM: shortcut for :class:`PriorityRandom`.
    :cvar ASCENDING: shortcut for :class:`PriorityAscending`. Can only compare candidates (not committees).
    :cvar DESCENDING: shortcut for :class:`PriorityDescending`. Can only compare candidates (not committees).
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def compare_committees(self, s, t) -> int:
        """
        Compare two committees.

        :param s: a committee.
        :param t: a committee.
        :return: 0 if `s == t`, -1 if the tie is broken in favor of `s` over `t`, 1 otherwise.
        """
        raise NotImplementedError

    def choose_committee(self, x: Union[set, list], reverse: bool = False) -> Union[set, None]:
        """
        Choose an element from a list, set, etc. of committees.

        :param x: the list, set, etc where the committee is to be chosen.
        :param reverse: if False (default), then we choose the "first" or "best" committee in this priority order. If
            True, then we choose the "last" or "worst" committee.
        :return: the chosen committee (or None). When ``x`` is empty, return None. When ``x`` has one element, return
            this element.
        """
        if len(x) == 0:
            return None
        if len(x) == 1:
            return list(x)[0]
        return self._choose_committee(x, reverse=reverse)

    def _choose_committee(self, x: Union[set, list], reverse: bool) -> set:
        """
        Auxiliary function for :meth:`choose`.

        Here, ``x`` is assumed to have at least 2 elements.
        """
        if reverse:
            return max(x, key=cmp_to_key(self.compare_committees))
        else:
            return min(x, key=cmp_to_key(self.compare_committees))

    def sort_committees(self, x: Union[set, list], reverse: bool = False) -> Union[list, None]:
        """
        Sort a list, set, etc. of committees.

        :param x: the list, set, etc.
        :param reverse: if True, we use the reverse priority order.
        :return: a sorted list (or None).

        The original list ``x`` is not modified.
        """
        if len(x) <= 1:
            return list(x)
        return self._sort_committees(x, reverse=reverse)

    def _sort_committees(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        """
        Auxiliary function for :meth:`sort`.

        Here, ``x`` is assumed to have at least 2 elements.
        """
        return sorted(x, key=cmp_to_key(self.compare_committees), reverse=reverse)

    def compare(self, c, d) -> int:
        """
        Compare two candidates.

        :param c: a candidate.
        :param d: a candidate.
        :return: 0 if `c == d`, -1 if the tie is broken in favor of `c` over `d`, 1 otherwise.
        """
        return self.compare_committees({c}, {d})

    def choose(self, x: Union[set, list], reverse: bool = False) -> object:
        """
        Choose an element from a list, set, etc.

        :param x: the list, set, etc where the element is to be chosen.
        :param reverse: if False (default), then we choose the "first" or "best" element in this priority order. For
            example, if this is the ascending priority, we choose the lowest element. If True, then we
            choose the "last" or "worst" element. This is used, for example, in :class:`RuleVeto`.
        :return: the chosen element (or None). When ``x`` is empty, return None. When ``x`` has one element, return
            this element.
        """
        if len(x) == 0:
            return None
        if len(x) == 1:
            return list(x)[0]
        return self._choose(x, reverse=reverse)

    def _choose(self, x: Union[set, list], reverse: bool) -> object:
        """
        Auxiliary function for :meth:`choose`.

        Here, ``x`` is assumed to have at least 2 elements.
        """
        if reverse:
            return max(x, key=cmp_to_key(self.compare))
        else:
            return min(x, key=cmp_to_key(self.compare))

    def sort(self, x: Union[set, list], reverse: bool = False) -> Union[list, None]:
        """
        Sort a list, set, etc.

        :param x: the list, set, etc.
        :param reverse: if True, we use the reverse priority order.
        :return: a sorted list (or None).

        The original list ``x`` is not modified.
        """
        if len(x) <= 1:
            return list(x)
        return self._sort(x, reverse=reverse)

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        """
        Auxiliary function for :meth:`sort`.

        Here, ``x`` is assumed to have at least 2 elements.
        """
        return sorted(x, key=cmp_to_key(self.compare), reverse=reverse)

    def sort_pairs_rp(self, x: Union[set, list], reverse: bool = False) -> Union[list, None]:
        """
        Sort a list, set, etc. of pairs of candidates (for Ranked Pairs).

        :param x: the list, set, etc.
        :param reverse: if True, we use the reverse priority order.
        :return: a sorted list (or None).

        By default, it is in the normal priority order for the first element of the pair, and in the reverse priority
        order for the second element of the pair.

        The original list ``x`` is not modified.
        """
        if len(x) <= 1:
            return list(x)
        return self._sort_pairs_rp(x=x, reverse=reverse)

    def _sort_pairs_rp(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        def compare_pairs(pair_1, pair_2):
            comp_left = self.compare(pair_1[0],  pair_2[0])
            if comp_left != 0:
                return comp_left
            return - self.compare(pair_1[1], pair_2[1])
        return sorted(x, key=cmp_to_key(compare_pairs), reverse=reverse)

    # Priority orders defined by default
    # ----------------------------------
    # The following constants are defined outside the class to avoid a problem of self-reference.

    UNAMBIGUOUS = None
    ABSTAIN = None
    ASCENDING = None
    DESCENDING = None
    RANDOM = None


class PriorityUnambiguous(Priority):
    """When there are two elements or more, raise a ValueError.

    >>> try:
    ...     Priority.UNAMBIGUOUS.choose({'a', 'b'})
    ... except ValueError:
    ...     print('Cannot choose')
    Cannot choose
    >>> try:
    ...     Priority.UNAMBIGUOUS.sort({'a', 'b'})
    ... except ValueError:
    ...     print('Cannot sort')
    Cannot sort
    """

    def __init__(self):
        super().__init__(name='Unambiguous')

    def __repr__(self):
        return 'Priority.UNAMBIGUOUS'

    def compare_committees(self, s, t) -> int:
        raise ValueError("%s cannot compare %r and %r." % (self, s, t))

    def _choose_committee(self, x: Union[set, list], reverse: bool) -> set:
        raise ValueError("%s cannot choose from %r." % (self, x))

    def _sort_committees(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        raise ValueError("%s cannot sort %r." % (self, x))

    def compare(self, c, d) -> int:
        raise ValueError("%s cannot compare %r and %r." % (self, c, d))

    def _choose(self, x: Union[set, list], reverse: bool) -> object:
        raise ValueError("%s cannot choose from %r." % (self, x))

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        raise ValueError("%s cannot sort %r." % (self, x))

    def _sort_pairs_rp(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        raise ValueError("%s cannot sort %r." % (self, x))


Priority.UNAMBIGUOUS = PriorityUnambiguous()


class PriorityAbstain(Priority):
    """
    When there are two elements or more, return None.

    >>> print(Priority.ABSTAIN.choose({'a', 'b'}))
    None
    >>> print(Priority.ABSTAIN.sort({'a', 'b'}))
    None
    """

    def __init__(self):
        super().__init__(name='Abstain')

    def __repr__(self):
        return 'Priority.ABSTAIN'

    def compare_committees(self, s, t) -> int:
        raise None

    def _choose_committee(self, x: Union[set, list], reverse: bool) -> Union[set, None]:
        return None

    def _sort_committees(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return None

    def compare(self, c, d) -> int:
        raise None

    def _choose(self, x: Union[set, list], reverse: bool) -> object:
        return None

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return None

    def _sort_pairs_rp(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return None


Priority.ABSTAIN = PriorityAbstain()


class PriorityRandom(Priority):
    """Random order.

    >>> my_choice = Priority.RANDOM.choose({'a', 'b'})
    >>> my_choice in {'a', 'b'}
    True
    >>> my_order = Priority.RANDOM.sort({'a', 'b'})
    >>> my_order == ['a', 'b'] or my_order == ['b', 'a']
    True
    """

    def __init__(self):
        super().__init__(name='Random')

    def __repr__(self):
        return 'Priority.RANDOM'

    def compare_committees(self, s, t) -> int:
        if s == t:
            return 0
        return random.choice([-1, 1])

    def _choose_committee(self, x: Union[set, list], reverse: bool) -> set:
        return random.choice(list(x))

    def _sort_committees(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return random.sample(x, len(x))

    def compare(self, c, d) -> int:
        if c == d:
            return 0
        return random.choice([-1, 1])

    def _choose(self, x: Union[set, list], reverse: bool) -> object:
        return random.choice(list(x))

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return random.sample(x, len(x))

    def _sort_pairs_rp(self, x: Union[set, list], reverse: bool):
        return random.sample(x, len(x))


Priority.RANDOM = PriorityRandom()


class PriorityCandidate(Priority):
    """
    A priority setting designed only to break ties between candidates, not between committees.

    For examples, cf. :class:`PriorityAscending` and :class:`PriorityDescending`.
    """
    # Main difference between :class`Priority` and :class:`PriorityCandidate`:
    #
    #   * In :class:`Priority`, you have to implement `compare_committees`, and `compare` is deduced from it.
    #   * In :class:`PriorityCandidate`, you have to implement `compare`, and `compare_committees` is deduced from it
    #     (only for committees of size 1).

    def compare(self, c, d):
        raise NotImplementedError

    def compare_committees(self, s, t) -> int:
        """
        Compare two committees.

        :param s: a committee.
        :param t: a committee.
        :return: 0 if `s == t`, -1 if the tie is broken in favor of `s` over `t`, 1 otherwise.
        """
        if len(s) == len(t) == 1:
            return self.compare(list(s)[0], list(t)[0])
        else:
            raise ValueError("%s cannot compare %r and %r." % (self, s, t))


class PriorityAscending(PriorityCandidate):
    """
    Ascending order on candidates (lowest is favoured).

    >>> Priority.ASCENDING.choose({'a', 'b'})
    'a'
    >>> Priority.ASCENDING.sort({'a', 'b'})
    ['a', 'b']
    >>> Priority.ASCENDING.sort_pairs_rp({('a', 'b'), ('b', 'a'), ('a', 'c')})
    [('a', 'c'), ('a', 'b'), ('b', 'a')]
    """

    def __init__(self):
        super().__init__(name='Ascending')

    def __repr__(self):
        return 'Priority.ASCENDING'

    def compare(self, c, d) -> int:
        if c == d:
            return 0
        return -1 if c < d else 1

    def _choose(self, x: Union[set, list], reverse: bool) -> object:
        if reverse:
            return max(x)
        return min(x)

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return sorted(x, reverse=reverse)


Priority.ASCENDING = PriorityAscending()


class PriorityDescending(PriorityCandidate):
    """
    Descending order on candidates (highest is favoured).

    >>> Priority.DESCENDING.choose({'a', 'b'})
    'b'
    >>> Priority.DESCENDING.sort({'a', 'b'})
    ['b', 'a']
    >>> Priority.DESCENDING.sort_pairs_rp({('a', 'b'), ('b', 'a'), ('a', 'c')})
    [('b', 'a'), ('a', 'b'), ('a', 'c')]
    """

    def __init__(self):
        super().__init__(name='Descending')

    def __repr__(self):
        return 'Priority.DESCENDING'

    def compare(self, c, d) -> int:
        if c == d:
            return 0
        return 1 if c < d else -1

    def _choose(self, x: Union[set, list], reverse: bool) -> object:
        if reverse:
            return min(x)
        return max(x)

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return sorted(x, reverse=not reverse)


Priority.DESCENDING = PriorityDescending()
