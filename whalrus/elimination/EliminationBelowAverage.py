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
from whalrus.utils.Utils import cached_property
from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.elimination.Elimination import Elimination
from whalrus.rule.RulePlurality import RulePlurality


class EliminationBelowAverage(Elimination):
    """
    Elimination of the candidates whose score is lower than the average score

    :param `*args`: cf. parent class.
    :param strict: if True (resp. False), then eliminate the candidates whose score is strictly lower than
        (resp. lower or equal to) the average.
    :param `**kwargs`: cf. parent class.

    >>> rule = RulePlurality(ballots=['a', 'b', 'c', 'd'], weights=[35, 30, 25, 10])
    >>> rule.gross_scores_
    {'a': 35, 'b': 30, 'c': 25, 'd': 10}
    >>> EliminationBelowAverage(rule=rule).eliminated_
    {'d'}
    >>> EliminationBelowAverage(rule=rule, strict=False).eliminated_
    {'c', 'd'}

    If no candidates should be eliminated (which may happen only if ``strict`` is True), then all candidates are
    eliminated.

    >>> rule = RulePlurality(ballots=['a', 'b'])
    >>> rule.gross_scores_
    {'a': 1, 'b': 1}
    >>> EliminationBelowAverage(rule=rule).eliminated_
    {'a', 'b'}
    """

    def __init__(self, *args, strict=True, **kwargs):
        self.strict = strict
        super().__init__(*args, **kwargs)

    def __call__(self, rule: RuleScoreNum):
        return super().__call__(rule=rule)

    @cached_property
    def eliminated_order_(self):
        if self.rule_.best_score_ == self.rule_.worst_score_:
            return self.rule_.order_
        worst_first = []
        for tie_class in self.rule_.order_[::-1]:
            some_candidate = list(tie_class)[0]
            score = self.rule_.scores_[some_candidate]
            if score < self.rule_.average_score_ or (not self.strict and score == self.rule_.average_score_):
                worst_first.append(tie_class)
            else:
                break
        return worst_first[::-1]
