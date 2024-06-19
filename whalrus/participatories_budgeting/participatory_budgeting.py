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

from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.profiles.profile import Profile
from whalrus.rules.rule import Rule
from whalrus.rules.rule_borda import RuleBorda
from whalrus.utils.utils import cached_property, my_division, NiceDict
import numpy as np

class ParticipatoryBudgeting(RuleCommittee):

    def __init__(self,*args, base_rule : Rule = None, project_cost : dict(), budget : float, **kwargs):

        self.base_rule = base_rule
        self.project_cost = project_cost
        self.budget = budget
        super().__init__(*args, **kwargs)
        for i in range(len(self.profile_converted_._voters)):
            if self.profile_converted_._voters[i] is None:
                self.profile_converted_._voters[i] = i

    

    @cached_property
    def intial_voters_budget(self):
        voters_budget = {}
        for i, voter in enumerate(self.profile_converted_.voters):
            voters_budget[voter] = my_division(self.profile_converted_.weights[i]*self.budget, np.sum(self.profile_converted_.weights))
        return NiceDict(voters_budget)

    @cached_property
    def base_rule_(self):
        return self.base_rule(ballots = self.profile_converted_, candidates = self.candidates_)

    @cached_property
    def initial_vote_counts(self):
        return self.base_rule_.gross_scores_

    @cached_property
    def intial_voters_utilities(self):
        all_utilities = {}
        for i, ballot_pack  in enumerate(self.profile_converted_.items()):
            ballot, weight, voter = ballot_pack
            all_utilities[voter] = {candidate: self.base_rule.scorer(ballot=ballot, candidates=self.candidates_).scores_[candidate]*weight
                    for candidate in self.candidates_}

        return all_utilities
            



if __name__ == '__main__':
    p = Profile(['a > b > c','b >c >a'], weights = [2,1])

    pb = ParticipatoryBudgeting(p, base_rule = RuleBorda(),
         project_cost = {'a':50, 'b':50, 'c':20}, budget = 120)
    

    print(pb.intial_voters_budget)