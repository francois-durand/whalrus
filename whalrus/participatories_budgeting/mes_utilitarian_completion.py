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
    tie_break : Priority
        PriorityBudgetingAscendingCount
    kwargs
        Cf. parent class.
    """
    def __init__(self,*args,tie_break = PriorityBudgetingAscendingCount(), **kwargs) -> None:
        super().__init__(*args,tie_break=tie_break, **kwargs)  


    def utilitarian_completion_(self, winners):
        cost_so_far = sum(self.project_cost[c] for c in winners)
        budget = self.budget - cost_so_far

        project_cost = {c:self.project_cost[c] for c in self.project_cost.keys() if c not in winners }
        result = Greedy(self.profile_converted_, base_rule = self.base_rule, project_cost = project_cost, budget = budget,
                        tie_break=self.tie_break, converter = self.converter)
        
        return winners + list(result.winners_), result.remaining_budget_

    @cached_property
    def completion_(self): #Only Equal Shares followed by utilitarian completion
        winners = self.rule_winners(self.budget)
        return self.utilitarian_completion_(winners)