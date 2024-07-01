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

    @cached_property
    def winners_(self):

        return NiceSet(self.greedy_method[-1].winners)

    @cached_property
    def greedy_method(self):
        
        steps = []
        remaining = copy.deepcopy(self.initial_vote_counts)
        budget_voter = copy.deepcopy(self.intial_voters_budget)
        wallet = VotersWallet(self.project_cost, self.voters_utilities,self.supporters)
        wallet(remaining,budget_voter)



        for c in wallet.remaining_sorted_:
            if not wallet.not_affordable(c):
                wallet.winners.append(c)
                budget_voter = wallet.updated_budget_(c)
            steps.append(copy.deepcopy(wallet))
            remaining = wallet.remaining
            wallet(remaining,budget_voter)

        return steps


        
