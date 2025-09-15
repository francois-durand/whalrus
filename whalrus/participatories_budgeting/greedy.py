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
from whalrus.utils.utils import DeleteCacheMixin, cached_property,\
                                    NiceSet, NiceDict,NiceFrozenSet
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule import Rule
from whalrus.participatories_budgeting.participatory_budgeting import ParticipatoryBudgeting
from whalrus.priorities.priority_budgeting import PriorityBudgetingDescendingCost
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union
import copy


class Greedy(ParticipatoryBudgeting):
    """
    Participatory budgeting rule that simply all most approved and affordable projects.

    Parameters
    ----------
    args 
        If present, these parameters will be passed to ``__call__`` immediately after initialization.
    tie_break : Priority
        Default : PriorityBudgetingAscendingCount
    kwargs 
        If present, these parameters will be passed to ``__call__`` immediately after initialization.

    Attributes 
    ---------
    winners : list
        This stores all the winners of each step from the first one to the actual
    tied : list 
        This stores all the ties of each step from the first one to the actual


    """
    
    def __init__(self,*args , tie_break = PriorityBudgetingDescendingCost(), **kwargs) -> None:
          
        super().__init__(*args, tie_break=tie_break, **kwargs)  
        
    def prepriority(self, selection):
        
        return [(c, 0, self.project_cost[c]) for c in selection]

    @cached_property
    def winners_(self):

        return self.greedy_method_[0]
    
    @cached_property
    def eliminated_(self):
        return self.greedy_method_[1]
    
    @cached_property
    def greedy_method_(self):
        winners, eliminated = [],[]
        remaining_budget = self.budget
        
        for projects in self.base_rule_.order_:
            for project in self.tie_break._sort(self.prepriority(projects)):
                if self.project_cost_[project] <= remaining_budget:
                    winners.append(project)
                    remaining_budget -= self.project_cost_[project]
                else:
                    eliminated.append(project)
        return NiceFrozenSet(winners), NiceFrozenSet(eliminated)

        
