import logging
from whalrus.participatories_budgeting.greedy import Greedy
from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule import Rule
from whalrus.rules.rule_borda import RuleBorda
from whalrus.utils.utils import cached_property, my_division, NiceDict, DeleteCacheMixin, NiceSet
from whalrus.priorities.priority_budgeting import PriorityBudgeting
from whalrus.priorities.priority_budgeting import PriorityBudgetingAscendingCount
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.participatories_budgeting.equal_shares import EqualShares 
from whalrus.participatories_budgeting.budgeting_completion import BudgetingCompletion
from typing import Union

import numpy as np


class MesUtilitarianCompletion(BudgetingCompletion):
    """
    Using the utilitarian completion when the Add1 completion fails.

    Parameters
    --------
    args
        Cf. parent class.
    kwargs
        Cf. parent class.
    """
    def __init__(self,*args,tie_break = PriorityBudgetingAscendingCount(), **kwargs) -> None:
        super().__init__(*args,tie_break=tie_break, **kwargs)  

    @cached_property
    def completed_winners_(self):
        return NiceSet(self.equal_shares_only[0])

    @cached_property
    def additionnal_cost(self):
        return self.equal_shares_only[1]


    def utilitarian_completion_(self, winners):
        cost_so_far = sum(self.project_cost[c] for c in winners)
        budget = self.budget - cost_so_far

        project_cost = {c:self.project_cost[c] for c in self.project_cost.keys() if c not in winners }
        result = Greedy(self.profile_converted_, base_rule = self.base_rule, project_cost = project_cost, budget = budget,
                        tie_break=self.tie_break, converter = self.converter)
        
        return winners + list(result.winners_), self.budget - result.remaining_budget_

    @cached_property
    def equal_shares_only(self): #Only Equal Shares followed by utilitarian completion
        winners = list(EqualShares(self.profile_converted_, budget = self.budget, project_cost = self.project_cost, base_rule = self.base_rule_).winners_)
        return self.utilitarian_completion_(winners)