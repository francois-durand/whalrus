import logging
from whalrus.utils.utils import DeleteCacheMixin, cached_property, NiceSet, NiceDict
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule import Rule
from whalrus.participatories_budgeting.voters_wallet_equal_shares import VotersWalletEqualShares
from whalrus.participatories_budgeting.participatory_budgeting import ParticipatoryBudgeting
from whalrus.priorities.priority_budgeting import PriorityBudgetingAscendingCount
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union
import copy

class BudgetingMethod(ParticipatoryBudgeting):
    """
    Solving participatory budgeting problem with different methods (such as :class:`EqualShares` and :class:`Greedy`)

    Parameters
    ----------
    args
        Cf. parent class.
    kwargs
        Cf. parent class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @cached_property
    def winners_(self):
        return self.get_results[0]
    
    @cached_property
    def eliminated_(self):
        return self.get_results[1]
    
    @cached_property
    def remaining_budget_(self):
        return self.get_results[2]

    @cached_property
    def get_results(self):
        raise NotImplementedError