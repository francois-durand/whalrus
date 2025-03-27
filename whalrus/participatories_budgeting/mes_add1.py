import logging
from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule import Rule
from whalrus.rules.rule_borda import RuleBorda
from whalrus.utils.utils import cached_property, my_division, NiceDict, DeleteCacheMixin, NiceSet
from whalrus.priorities.priority_budgeting import PriorityBudgeting
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.participatories_budgeting.equal_shares import EqualShares
from whalrus.participatories_budgeting.mes_utilitarian_completion import MesUtilitarianCompletion
from typing import Union

import numpy as np

class MesAdd1(EqualShares):
    
    def __init__(self,*args, add1u = False, stop_exhaustion = True, integral_endowments = False, **kwargs) -> None:
        self.add1u = add1u
        self.stop_exhaustion = stop_exhaustion
        self.integral_endowments = integral_endowments
        super().__init__(*args, **kwargs) 

    @cached_property
    def completed_winners_(self):
        return NiceSet(self.equal_shares) 

    @cached_property
    def equal_shares(self):
        
        mes = list(self.winners_)
        if self.integral_endowments:
            budget = int(self.budget / len(self.voters_)) * len(self.voters_)
        else:
            budget = self.budget
        current_cost = sum(self.project_cost[c] for c in mes)
        while True:
            is_exhaustive = True
            for extra in self.candidates_:
                if extra not in mes and current_cost + self.project_cost[extra] <= self.budget:
                    is_exhaustive = False
                    break
            if is_exhaustive and self.stop_exhaustion:
               break
            
            next_budget = budget + len(self.voters_)
            next_mes = list(EqualShares(self.profile_original_, budget = next_budget, project_cost = self.project_cost, base_rule = self.base_rule_).winners_)
            current_cost = sum(self.project_cost[c] for c in next_mes)
            if current_cost <= self.budget:
                budget = next_budget
                mes = next_mes
            else:
                break 
            
        if self.add1u:
            mes = MesUtilitarianCompletion(self.profile_converted_, budget = self.budget, project_cost = self.project_cost, base_rule = self.base_rule_).utilitarian_completion_(mes)[0]
        return mes