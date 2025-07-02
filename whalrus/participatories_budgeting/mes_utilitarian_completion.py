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
from typing import Union

import numpy as np

# Maybe redundant. Could be completly integrated to mes_add1 (unless we really want to do only this completion) and by using
#     directly the greedy method instead. (not sure about this)
class MesUtilitarianCompletion(EqualShares):
    """
    Using the utilitarian completion when the Add1 completion fails.

    Parameters
    --------
    args
        Cf. parent class.
    kwargs
        Cf. parent class.
    """
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)  

    @cached_property
    def completed_winners_(self):
        return NiceSet(self.equal_shares[0])

    @cached_property
    def additionnal_cost(self):
        return self.equal_shares[1]

    
    def utilitarian_completion_(self, winners): #same as doing greddy over Equal Shares output
        cost_so_far = sum(self.project_cost[c] for c in winners)
        sorted_projects = sorted(self.candidates_, key = lambda c: len(self.supporters[c]), reverse = True)

        for c in sorted_projects:
            if c in winners or cost_so_far + self.project_cost[c] > self.budget:
                continue
            winners.append(c)
            cost_so_far += self.project_cost[c]
        return winners, cost_so_far

    @cached_property
    def equal_shares(self):
        winners = list(self.winners_)
        return self.utilitarian_completion_(winners)