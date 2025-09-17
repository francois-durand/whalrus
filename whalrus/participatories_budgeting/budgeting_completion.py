import logging
from whalrus.utils.utils import DeleteCacheMixin, cached_property, NiceSet, NiceDict
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule import Rule
from whalrus.participatories_budgeting.equal_shares import EqualShares
from whalrus.participatories_budgeting.participatory_budgeting import ParticipatoryBudgeting
from whalrus.priorities.priority_budgeting import PriorityBudgetingAscendingCount
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union
import copy

class BudgetingCompletion(ParticipatoryBudgeting):

    def __init__(self, *args,rule = None, **kwargs):
        super().__init__(*args, **kwargs)
        if rule is None:
            rule = EqualShares(self.profile_converted_, budget = self.budget,
                                project_cost = self.project_cost,
                                base_rule = self.base_rule_)
        self.rule = rule
        

    def rule_winners(self, budget):
        return list(self.rule(self.profile_converted_, budget = budget, project_cost = self.project_cost).winners_)


    