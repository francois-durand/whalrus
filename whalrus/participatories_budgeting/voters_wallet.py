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

class VotersWallet(DeleteCacheMixin):

    def __init__(self,project_cost,total_utility,supporters):
        self.project_cost = project_cost
        self.supporters = supporters 
        self.total_utility = total_utility
        self.eliminated = {}
        self.winners = []
        

    def __call__(self, remaining, budget):
        self.best = []
        self.remaining = remaining
        
        self.budget = budget
        self.delete_cache()
        return self
     
    def not_affordable(self, c):
       
        if self.budget < self.project_cost[c]:
            self.eliminated[c] = copy.copy(self.remaining[c])
            del self.remaining[c]
            return True
        return False
    
    def sorted_supporters(self, c):
        return sorted(self.supporters[c],key = lambda i : self.voter_budget[i]/self.total_utility[i][c] )
    
    def updated_budget_(self, c):
        return self.budget - self.project_cost[c]


    @cached_property
    def remaining_sorted_(self):
        return sorted(self.remaining, key=lambda c: self.remaining[c], reverse=True)
          
   
   



