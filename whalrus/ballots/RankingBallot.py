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
import numpy as np


class RankingBallot:
    """
    A ballot giving a pre-order on a subset of candidates.
    The first item of the list is the preferred one.

    >>> ballot = RankingBallot({'a': 4., 'b': 4., 'c': 3., 'd': 2.,
    ...                         'e': np.nan})
    """
    def __init__(self, b):
        # if type(b) == dict:
        #     super().__init__(b)
        #
        # elif type(b) in [list, tuple, set]:  # changer en iterable
        #     super().__init__({x: i for i, x in enumerate(reversed(list(b)))})
        #
        # else:
        #     raise TypeError('expecting dict,list,tuple or set')
        # TODO: the input method must be changed (not to involve utilities)
        self._utilities = b
        self.candidates = self._utilities.keys()
        pass

    def strictly_prefer(self, c1, c2):
        """
        Whether one candidate is preferred to another.

        :param c1: a candidate.
        :param c2: another candidate.
        :return: if both candidates are in the weak order, then return True if
            c1 is strictly preferred to c2, and False otherwise (including
            when c1 is equivalent to c2). If at least one of the candidates
            is not in the weak order, then return None.

        >>> ballot = RankingBallot({'a': 4., 'b': 4., 'c': 3., 'd': 2.,
        ...                         'e': np.nan})
        >>> ballot.strictly_prefer('a', 'c')
        True
        >>> ballot.strictly_prefer('a', 'b')
        False
        >>> print(ballot.strictly_prefer('a', 'e'))
        None
        >>> print(ballot.strictly_prefer('a', 'z'))
        None
        """
        if (c1 not in self.candidates
                or c2 not in self.candidates
                or np.isnan(self._utilities[c1])
                or np.isnan(self._utilities[c2])):
            return None
        return self._utilities[c1] > self._utilities[c2]

    def top_candidate(self, election_candidates=None):
        """
        The top candidate

        :param election_candidates: the set of candidates from which we want
            the top candidate of the voter. By default, it is the set of
            candidates mentioned in her ballot. But in general, it can be a
            subset, a superset, etc.
        :return: the preferred candidate of the voter, in the intersection of
            :attr:`election_candidates` and the candidates mentionned in the
            ballot. If that is not possible (because of a tie, or because the
            intersection is empty, etc.), then return None.

        >>> ballot = RankingBallot({'a': 4., 'b': 3., 'c': 3., 'd': 2.,
        ...                         'e': np.nan})
        >>> print(ballot.top_candidate())
        a
        >>> print(ballot.top_candidate({'b', 'd', 'e'}))
        b
        >>> print(ballot.top_candidate({'b', 'c', 'd', 'e'}))
        None
        >>> print(ballot.top_candidate({'b', 'c', 'd', 'e', 'f'}))
        None
        >>> print(ballot.top_candidate({'f', 'g'}))
        None
        >>> print(ballot.top_candidate({'e'}))
        None
        """
        if election_candidates is None:
            election_candidates = self.candidates
        utilities_intersection = {
            c: self._utilities[c]
            for c in election_candidates if c in self._utilities.keys()
        }
        if not utilities_intersection:
            return None
        max_utility = max(utilities_intersection.values())
        favorites = [c for c in utilities_intersection.keys()
                     if utilities_intersection[c] == max_utility]
        if len(favorites) == 1:
            return favorites[0]
        else:
            return None


if __name__ == '__main__':

    import doctest
    doctest.testmod()
