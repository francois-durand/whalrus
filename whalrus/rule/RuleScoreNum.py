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
from whalrus.rule.RuleScore import RuleScore
from whalrus.utils.Utils import cached_property, NiceDict, NiceSet, my_division
from numbers import Number


class RuleScoreNum(RuleScore):
    """
    A voting rule with numeric scores.

    This is a voting rule where each candidate is assigned a numeric score, and the candidates with the best
    score are declared the cowinners.
    """

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The scores.

        :return: a :class:`NiceDict` that, to each candidate, assigns a numeric score.
        """
        raise NotImplementedError

    def compare_scores(self, one: Number, another: Number) -> int:
        if one == another:
            return 0
        return -1 if one < another else 1

    @cached_property
    def best_score_(self) -> Number:
        return max(self.scores_.values())

    @cached_property
    def worst_score_(self) -> Number:
        return min(self.scores_.values())

    @cached_property
    def average_score_(self) -> Number:
        """
        The average score.

        :return: the average score.
        """
        return my_division(sum(self.scores_.values()), self.n_candidates_)

    @cached_property
    def order_(self) -> list:
        return [NiceSet(k for k in self.scores_.keys() if self.scores_[k] == v)
                for v in sorted(set(self.scores_.values()), reverse=True)]

    # Conversion to floats
    # --------------------

    @cached_property
    def scores_as_floats_(self) -> NiceDict:
        """
        Scores as floats.

        :return: :attr:`scores_` converted to floats.
        """
        return NiceDict({c: float(v) for c, v in self.scores_.items()})

    @cached_property
    def best_score_as_float_(self) -> Number:
        """
        The best score as a float.

        :return: :attr:`RuleScore.best_score_` converted to a float.
        """
        # noinspection PyTypeChecker
        return float(self.best_score_)

    @cached_property
    def worst_score_as_float_(self) -> Number:
        """
        The worst score as a float.

        :return: :attr:`RuleScore.worst_score_` converted to a float.
        """
        # noinspection PyTypeChecker
        return float(self.worst_score_)

    @cached_property
    def average_score_as_float_(self) -> Number:
        """
        The average score as a float.

        :return: :attr:`average_score_` converted to a float.
        """
        # noinspection PyTypeChecker
        return float(self.average_score_)
