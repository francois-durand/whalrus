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
import numpy as np
from whalrus.utils.utils import DeleteCacheMixin, cached_property, NiceSet, set_to_list, NiceDict
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union
import copy

class VotersWalletEqualShares(DeleteCacheMixin):

    def __init__(self,project_cost,total_utility,supporters):
        self.project_cost = project_cost
        self.supporters = supporters 
        self.total_utility = total_utility
        self.eliminated = {}
        self.winners = []
        

    def __call__(self, remaining, voter_budget):
        self.best_eff_vote_count = 0
        self.best = []
        self.remaining = remaining
        
        self.voter_budget = voter_budget
        self.delete_cache()
        return self
     
    def not_affordable(self, c):
        approver_amount = sum(self.voter_budget[voter] for voter in self.supporters[c])
              
        if approver_amount < self.project_cost[c]:
            self.eliminated[c] = copy.copy(self.remaining[c])
            del self.remaining[c]
            return True
        return False
    
    def sorted_supporters(self, c):
        return sorted(self.supporters[c],key = lambda i : self.voter_budget[i]/self.total_utility[i][c] )
    
    def updated_budget_(self, best):
        best_max_payment = self.project_cost[best] / self.best_eff_vote_count
        updated_budget = copy.copy(self.voter_budget)
        for voter in self.supporters[best]:
            payment = best_max_payment*self.total_utility[voter][best]
            updated_budget[voter] = max(0, self.voter_budget[voter] - payment)

        return updated_budget

    def get_share_count(self, c):
        amount_so_far = 0
        d = self.remaining[c]
        for voter in self.sorted_supporters(c):
            payment_factor = (self.project_cost[c] - amount_so_far)/d
            eff_vote_count = self.project_cost[c] / payment_factor
            
            if payment_factor*self.total_utility[voter][c] > self.voter_budget[voter]:
                amount_so_far += self.voter_budget[voter]
                d -= self.total_utility[voter][c]
            else:
                self.remaining[c] = eff_vote_count
                
                if eff_vote_count > self.best_eff_vote_count:
                    self.best_eff_vote_count = eff_vote_count
                    self.best = [(c, eff_vote_count, self.project_cost[c])]
                elif eff_vote_count == self.best_eff_vote_count:
                    self.best.append((c, eff_vote_count, self.project_cost[c]))
                break
      
        return self.best_eff_vote_count
 

    @cached_property
    def remaining_sorted_(self):
        return sorted(self.remaining, key=lambda c: self.remaining[c], reverse=True)
          
   
    @cached_property
    def best_shares_(self):
        
        for c in self.remaining_sorted_:
            p_eff_vote_count = self.remaining[c] 
            if p_eff_vote_count < self.best_eff_vote_count:
                break

            if self.not_affordable(c):
                continue

            self.best_eff_vote_count = self.get_share_count(c)
        if self.remaining:
            self.remaining_ = copy.copy(self.remaining)
        if self.best:
            self.winners.append([best[0] for best in self.best])
        return self.best
            

    
       



# for c in remaining_sorted:
            #     p_eff_vote_count = remaining[c]
            #     if p_eff_vote_count < best_eff_vote_count:
            #         break
            #     approver_amount = sum(budget_voter[voter] for voter in supporters[c])
              
            #     if approver_amount < self.project_cost[c]:
            #         del remaining[c]
            #         continue

            #     supporters[c].sort(key = lambda i : budget_voter[i]/self.voters_utilities[i][c])
            #     amount_so_far = 0
            #     d = remaining[c]
     
            #     for voter in supporters[c]:
            #         payment_factor = (self.project_cost[c] - amount_so_far)/d
            #         eff_vote_count = self.project_cost[c] / payment_factor
            #         if payment_factor*self.voters_utilities[voter][c] > budget_voter[voter]:
            #             amount_so_far += budget_voter[voter]
            #             d -= self.voters_utilities[voter][c]
            #         else:
            #             remaining[c] = eff_vote_count
                       
            #             if eff_vote_count > best_eff_vote_count:
            #                 best_eff_vote_count = eff_vote_count
            #                 best = [(c, eff_vote_count, self.project_cost[c])]
            #             elif eff_vote_count == best_eff_vote_count:
            #                 best.append((c, eff_vote_count, self.project_cost[c]))
            #             break
        
    
     