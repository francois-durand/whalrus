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
from whalrus.utils.utils import DeleteCacheMixin, cached_property, NiceSet
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule import Rule
from whalrus.participatories_budgeting.participatory_budgeting import ParticipatoryBudgeting
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union
import copy

class EqualShares(ParticipatoryBudgeting):

    def __init__(self,*args ,  **kwargs) -> None:
        super().__init__(*args,  **kwargs)    


    @cached_property
    def shares_(self):
        
        winners = []
        remaining = copy.deepcopy(self.initial_vote_counts)
        budget_voter = copy.deepcopy(self.intial_voters_budget)
     
        supporters = self.supporters
        while True:
            best_eff_vote_count = 0
            remaining_sorted = sorted(remaining, key=lambda c: remaining[c], reverse=True)
            for c in remaining_sorted:
                p_eff_vote_count = remaining[c]
                if p_eff_vote_count < best_eff_vote_count:
                    break
                approver_amount = sum(budget_voter[voter] for voter in supporters[c])
                if approver_amount < self.project_cost[c]:
                    del remaining[c]
                    continue

                supporters[c].sort(key = lambda i : budget_voter[i])
                amount_so_far = 0
                d = remaining[c]
                for voter in supporters[c]:
                    payment_factor = (self.project_cost[c] - amount_so_far)/d
                    eff_vote_count = self.project_cost[c] / payment_factor
                    if payment_factor*self.voters_utilities[voter][c] > budget_voter[voter]:
                        amount_so_far += budget_voter[voter]
                        d -= self.voters_utilities[voter][c]
                    else:
                        remaining[c] = eff_vote_count
                        if eff_vote_count >= best_eff_vote_count:
                            best_eff_vote_count = eff_vote_count
                            best = c
                        
                        break

            if not best:
                break
            winners.append(best)
            del remaining[best]
            best_max_payment = self.project_cost[best] / best_eff_vote_count
            for voter in supporters[c]:
                budget_voter[voter] = max(0, budget_voter[voter] - best_max_payment)

        return winners
