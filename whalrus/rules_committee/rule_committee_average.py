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
from whalrus.utils.utils import cached_property, NiceSet, NiceFrozenSet, NiceDict, my_division
from whalrus.priorities.priority import Priority
from whalrus.priorities.priority_lifted_leximax import PriorityLiftedLeximax
from whalrus.rules_committee.rule_committee_scoring import RuleCommitteeScoring
from whalrus.scorers.scorer import Scorer
from itertools import combinations

    
    
class RuleCommitteeAverage(RuleCommitteeScoring):

    def __init__(self, *args,base_rule = None, **kwargs):
        self.base_rule = base_rule
        super().__init__(*args, **kwargs)    
    
    @cached_property
    def base_rule_(self):
        return self.base_rule(ballots = self.profile_converted_, candidates = self.candidates_)

    def _cc_score(self, committee):
        return sum(
                self.base_rule_.scores_[candidate] for candidate in committee
        )

    def _cc_gross_scores(self, committee):
        return sum(
                self.base_rule_.gross_scores_[candidate] for candidate in committee
        )
