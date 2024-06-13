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
from whalrus.utils.utils import cached_property, NiceSet
from whalrus.selections.selection import Selection
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.priorities.priority import Priority
from whalrus.rules.rule_score_num import RuleScoreNum
from whalrus.profiles.profile import Profile
from whalrus.converters_ballot.converter_ballot_to_plurality import ConverterBallotToPlurality
from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder

class SelectionAbove(Selection):
    """
    Selection of the candidates whose score is greater than the specified quota


    Parameters
    ----------
    args
        Cf. parent class.
    strict : bool
        If True (resp. False), then select the candidates whose score is strictly greater than (resp. greater or equal
        to) the average.
    kwargs
        Cf. parent class.

    Examples
    --------
        >>> rule = RulePlurality(ballots=['a', 'b', 'c', 'd'], weights=[35, 30, 25, 10])
        >>> rule.gross_scores_
        {'a': 35, 'b': 30, 'c': 25, 'd': 10}
        >>> SelectionAbove(rule=rule, threshold = 25, strict = True).selected_
        {'a', 'b'}
        >>> SelectionAbove(rule=rule, threshold = 25).selected_
        {'a', 'b', 'c'}
    """

    def __init__(self, *args,threshold = 0, strict=False, transfert = False, **kwargs):
        self.strict = strict
        self.threshold = threshold 
        self.transfert = transfert
        super().__init__(*args, **kwargs)

    def __call__(self, rule):
        return super().__call__(rule=rule)

    @cached_property
    def selected_order_(self):
        best_first = []
        for tie_class in self.rule_.order_:
            some_candidate = list(tie_class)[0]
            score = self.rule_.gross_scores_[some_candidate]
            if score > self.threshold or (not self.strict and score == self.threshold):
                best_first.append(tie_class)
            else:
                break
        return best_first[::-1]
