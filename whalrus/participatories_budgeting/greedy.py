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

import logging
from whalrus.utils.utils import DeleteCacheMixin, cached_property, NiceSet, NiceDict
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule import Rule
from whalrus.participatories_budgeting.voters_wallet import VotersWallet
from whalrus.participatories_budgeting.participatory_budgeting import ParticipatoryBudgeting
from whalrus.priorities.priority_budgeting import PriorityBudgetingAscendingCount
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union
import copy


class Greedy(ParticipatoryBudgeting):

    
    def __init__(self,*args , tie_break = PriorityBudgetingAscendingCount(), **kwargs) -> None:
        super().__init__(*args, tie_break=tie_break, **kwargs)    
        self.winners = []
        self.tied = []

    def __call__(self,ballots: list | Profile = None, weights: list = None, voters: list = None, candidates: set = None):
        return super().__call__(ballots, weights, voters, candidates)
        
    def prepriority(self, cowinners):
        
        return [(c, 0, self.project_cost[c]) for c in cowinners]

    @cached_property
    def winners_(self):

        return NiceSet(self.greedy_method_[-1].winners)
    
    @cached_property
    def eliminated_(self):
        return NiceSet(self.eliminated)

    @cached_property
    def get_tied_selection_(self):

        return [step.tied for step in self.greedy_method_]

    @cached_property
    def greedy_method_(self):
        steps = []

        while True:

            best = self.base_rule_.cowinners_
            self.tied.append(best)
            best = self.tie_break._choose(self.prepriority(best))
            candidates = self.candidates_ - set(best)
            if self.project_cost[best] <= self.budget:
                self.winners.append(best)
                self.budget -= self.project_cost[best]
            else:
                self.eliminated.append(best) 
            steps.append(copy.deepcopy(self))
            if len(candidates) == 0:
                break
            self( self.profile_converted_, candidates = candidates)
            

        return steps

        
 