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
from whalrus.rules.rule import Rule
from whalrus.utils.utils import cached_property, NiceDict, NiceSet
from functools import cmp_to_key


class RuleScore(Rule):
    """
    A voting rule with scores (which are not necessarily numbers).

    Each candidate is assigned a score (not necessarily a number), and the the cowinners are the candidates with the
    best score, in the sense defined by :meth:`compare_scores`.
    """

    @cached_property
    def scores_(self) -> NiceDict:
        """NiceDict: The scores. To each candidate, this dictionary assigns a score (non necessarily a number).
        """
        raise NotImplementedError

    def compare_scores(self, one: object, another: object) -> int:
        """
        Compare two scores.

        Parameters
        ----------
        one : object
            A score.
        another : object
            A score.

        Returns
        -------
        int
            0 if they are equal, a positive number if ``one`` is greater than ``another``, a negative number otherwise.
        """
        raise NotImplementedError

    @cached_property
    def best_score_(self) -> object:
        """object: The best score.
        """
        return max(self.scores_.values(), key=cmp_to_key(self.compare_scores))

    @cached_property
    def worst_score_(self) -> object:
        """object: The worst score.
        """
        return min(self.scores_.values(), key=cmp_to_key(self.compare_scores))

    @cached_property
    def cowinners_(self):
        """NiceSet: Cowinners. The set of candidates with the best score.
        """
        return NiceSet({k for k, v in self.scores_.items() if v == self.best_score_})

    @cached_property
    def cotrailers_(self):
        """NiceSet: "Cotrailers". The set of candidates with the worst score.
        """
        return NiceSet({k for k, v in self.scores_.items() if v == self.worst_score_})

    @cached_property
    def order_(self) -> list:
        """list: Result of the election as a (weak) order over the candidates. It is a list of :class:`NiceSet`. The
        first set contains the candidates that have the best score, the second set contains those with the second best
        score, etc.
        """
        return [NiceSet(k for k in self.scores_.keys() if self.scores_[k] == v)
                for v in sorted(set(self.scores_.values()), key=cmp_to_key(self.compare_scores), reverse=True)]
