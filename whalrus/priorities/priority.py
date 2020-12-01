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

    Parameters
    ----------
    name : str
        The name of this priority setting.

    Attributes
    ----------
    UNAMBIGUOUS
        Shortcut for :class:`PriorityUnambiguous`.
    ABSTAIN
        Shortcut for :class:`PriorityAbstain`.
    ASCENDING
        Shortcut for :class:`PriorityAscending`.
    DESCENDING
        Shortcut for :class:`PriorityDescending`.
    RANDOM
        Shortcut for :class:`PriorityRandom`.

    Examples
    --------
    Typical usage:

        >>> priority = Priority.ASCENDING
        >>> priority.choice({'c', 'a', 'b'})
        'a'
        >>> priority.sort({'c', 'a', 'b'})
        ['a', 'b', 'c']
    """

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        """
        Examples
        --------
            >>> str(Priority.ASCENDING)
            'Ascending'
        """
        return self.name

    def compare(self, c, d) -> int:
        """
        Compare two candidates.

        Parameters
        ----------
        c : candidate
        d : candidate.

        Returns
        -------
        int
            0 if `c = d`, -1 if the tie is broken in favor of `c` over `d`, 1 otherwise.
        """
        raise NotImplementedError

    def choice(self, x: Union[set, list], reverse: bool = False) -> object:
        """
        Choose an element from a list, set, etc.

        Parameters
        ----------
        x : list, set, etc.
            The list, set, etc where the element is to be chosen.
        reverse : bool
            If False (default), then we choose the "first" or "best" element in this priority order. For example, if
            this is the ascending priority, we choose the lowest element. If True, then we choose the "last" or "worst"
            element. This is used, for example, in :class:`RuleVeto`.

        Returns
        -------
        object
            The chosen element (or None). When ``x`` is empty, return None. When ``x`` has one element, return this
            element.
        """
        if len(x) == 0:
            return None
        if len(x) == 1:
            return list(x)[0]
        return self._choice(x, reverse=reverse)

    def _choice(self, x: Union[set, list], reverse: bool) -> object:
        """
        Auxiliary function for :meth:`choice`.

        Here, ``x`` is assumed to have at least 2 elements.
        """
        if reverse:
            return max(x, key=cmp_to_key(self.compare))
        else:
            return min(x, key=cmp_to_key(self.compare))

    def sort(self, x: Union[set, list], reverse: bool = False) -> Union[list, None]:
        """
        Sort a list, set, etc.

        The original list ``x`` is not modified.

        Parameters
        ----------
        x : list, set, etc.
        reverse : bool
            If True, we use the reverse priority order.

        Returns
        -------
        list or None
            A sorted list (or None).
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

        By default, it is in the normal priority order for the first element of the pair, and in the reverse priority
        order for the second element of the pair.

        The original list ``x`` is not modified.

        Parameters
        ----------
        x : list, set, etc.
        reverse : bool
            If True, we use the reverse priority order.

        Returns
        -------
        list or None
            A sorted list (or None).
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
    """
    When there are two elements or more, raise a ValueError.

    Examples
    --------
        >>> try:
        ...     Priority.UNAMBIGUOUS.choice({'a', 'b'})
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

    def compare(self, c, d) -> int:
        raise ValueError("Cannot compare %r and %r with priority set to Unambiguous." % (c, d))

    def _choice(self, x: Union[set, list], reverse: bool) -> object:
        raise ValueError("Cannot choose from %r with priority set to Unambiguous." % x)

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        raise ValueError("Cannot sort %r with priority set to Unambiguous." % x)

    def _sort_pairs_rp(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        raise ValueError("Cannot sort %r with priority set to Unambiguous." % x)


Priority.UNAMBIGUOUS = PriorityUnambiguous()


class PriorityAbstain(Priority):
    """
    When there are two elements or more, return None.

    Examples
    --------
        >>> print(Priority.ABSTAIN.choice({'a', 'b'}))
        None
        >>> print(Priority.ABSTAIN.sort({'a', 'b'}))
        None
    """

    def __init__(self):
        super().__init__(name='Abstain')

    def __repr__(self):
        return 'Priority.ABSTAIN'

    def compare(self, c, d) -> int:
        return None

    def _choice(self, x: Union[set, list], reverse: bool) -> object:
        return None

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return None

    def _sort_pairs_rp(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return None


Priority.ABSTAIN = PriorityAbstain()


class PriorityAscending(Priority):
    """
    Ascending order (lowest is favoured).

    Examples
    --------
        >>> Priority.ASCENDING.choice({'a', 'b'})
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

    def _choice(self, x: Union[set, list], reverse: bool) -> object:
        if reverse:
            return max(x)
        return min(x)

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return sorted(x, reverse=reverse)


Priority.ASCENDING = PriorityAscending()


class PriorityDescending(Priority):
    """
    Descending order (highest is favoured).

    Examples
    --------
        >>> Priority.DESCENDING.choice({'a', 'b'})
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

    def _choice(self, x: Union[set, list], reverse: bool) -> object:
        if reverse:
            return min(x)
        return max(x)

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return sorted(x, reverse=not reverse)


Priority.DESCENDING = PriorityDescending()


class PriorityRandom(Priority):
    """
    Random order.

    Examples
    --------
        >>> my_choice = Priority.RANDOM.choice({'a', 'b'})
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

    def compare(self, c, d) -> int:
        if c == d:
            return 0
        return random.choice([-1, 1])

    def _choice(self, x: Union[set, list], reverse: bool) -> object:
        return random.choice(list(x))

    def _sort(self, x: Union[set, list], reverse: bool) -> Union[list, None]:
        return random.sample(x, len(x))

    def _sort_pairs_rp(self, x: Union[set, list], reverse: bool):
        return random.sample(x, len(x))


Priority.RANDOM = PriorityRandom()
