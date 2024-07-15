import logging
from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule import Rule
from whalrus.rules.rule_approval import RuleApproval
from whalrus.utils.utils import cached_property, my_division, NiceDict, DeleteCacheMixin, NiceSet
from whalrus.priorities.priority_budgeting import PriorityBudgeting
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.participatories_budgeting.mes_add1 import MesAdd1 
from typing import Union

import numpy as np

def test():

    p = Profile([{"p1": 1, "p2": 1, "p3":0}, {"p1": 1, "p2": 0, "p3":0}, {"p1": 0, "p2": 0, "p3":1}])

    mes = MesAdd1(p, project_cost = {"p1": 100, "p2": 50, "p3": 50}, budget = 150, 
    base_rule = RuleApproval(), add1u = True, stop_exhaustion = True, integral_endowments = True)

    assert mes.completed_winners_ == {'p1', 'p3'}