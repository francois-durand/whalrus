import logging
from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule import Rule
from whalrus.rules.rule_borda import RuleBorda
from whalrus.utils.utils import cached_property, my_division, NiceDict, DeleteCacheMixin, NiceSet
from whalrus.priorities.priority_budgeting import PriorityBudgeting
from whalrus.participatories_budgeting.budgeting_completion import BudgetingCompletion
from whalrus.participatories_budgeting.participatory_budgeting import ParticipatoryBudgeting
from whalrus.participatories_budgeting.equal_shares import EqualShares
from whalrus.participatories_budgeting.mes_utilitarian_completion import MesUtilitarianCompletion
from whalrus.priorities.priority_budgeting import PriorityBudgetingAscendingCount
from typing import Union

import numpy as np

class MesAdd1(BudgetingCompletion):
    """
    Completion method for Method of Equal Shares (MES).
    Sometimes the method of Equal Share output a suboptimal solution in the sense that the budget hasn't been fully spent.
    Thus, it's needed to find way to select others projects that can be funded.
    It virtually adds one currency unit (Add1) to every voters at each step until the sum of selected projects is greater
    than the total bugdet (initial)
    
    Parameters
    ----------
    args
        Cf. parent class.
    add1u : bool
        Default : False
        Sometimes, even Add1 fails to complete the completion.
        Specify if the completition should be followed by an utilitarian completion, which select the remaining projects 
        available by using a greedy method.
    stop_exhaustion : bool
        Default : True
        Stop the process when exhaustive.
    integral_endowments : bool
        Default : False
        Give each voters an integer when the budget is distributed
    kwargs
        Cf. parent class.
    """
    def __init__(self,*args, add1u = False, stop_exhaustion = True,tie_break = PriorityBudgetingAscendingCount(), integral_endowments = False, **kwargs):
        self.add1u = add1u
        self.stop_exhaustion = stop_exhaustion
        self.integral_endowments = integral_endowments
        self.tie_break = tie_break
        super().__init__(*args,tie_break=tie_break, **kwargs) 

   

    @cached_property  
    def completion_(self):
        
        mes = self.rule_winners(self.budget)
        if self.integral_endowments:
            budget = int(self.budget / len(self.voters_)) * len(self.voters_)
        else:
            budget = self.budget
        current_cost = sum(self.project_cost[c] for c in mes)
        while True:
            is_exhaustive = True
            new_budget = self.budget - current_cost
            for extra in self.candidates_:
                if extra not in mes and current_cost + self.project_cost[extra] <= budget:
                    is_exhaustive = False
                    break
            if is_exhaustive and self.stop_exhaustion:
               break
            
            next_budget = budget + len(self.voters_)
            next_mes = self.rule_winners(next_budget)    
            current_cost = sum(self.project_cost[c] for c in next_mes)
            if current_cost <= self.budget:
                budget = next_budget
                mes = next_mes
            else:
                break 
        
        if self.add1u:
            mes, new_budget  = MesUtilitarianCompletion(self.profile_converted_, budget = self.budget, project_cost = self.project_cost,
                                            base_rule = self.base_rule_, tie_break = self.tie_break).utilitarian_completion_(mes)
        return mes, new_budget 