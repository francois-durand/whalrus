import logging
from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.priorities.priority import Priority
from whalrus.priorities.priority_budgeting import PriorityBudgetingDescendingCost
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

def test_pathological():

    p = Profile([
        {"F2":1,"F3":1,"P3":0,"S2":0,"V1":0,"M1":1,"M3":1},
        {"F2":1,"F3":1,"P3":0,"S2":0,"V1":0,"M1":1,"M3":1},
        {"F2":0,"F3":0,"P3":1,"S2":1,"V1":0,"M1":0,"M3":0},
        {"F2":1,"F3":1,"P3":0,"S2":1,"V1":0,"M1":0,"M3":0},
        {"F2":1,"F3":1,"P3":0,"S2":0,"V1":1,"M1":0,"M3":0},
        {"F2":0,"F3":0,"P3":0,"S2":0,"V1":1,"M1":0,"M3":1},
        {"F2":0,"F3":0,"P3":0,"S2":0,"V1":1,"M1":1,"M3":1}])


    cc = MesAdd1(p, project_cost = {"F2":20,"F3":30,"P3":30, "S2":20,"V1":10,"M1":10,"M3":30},integral_endowments = True, stop_exhaustion = True, budget = 70, base_rule = RuleApproval(), tie_break = PriorityBudgetingDescendingCost(count = True))
    assert cc.completed_winners_ == {'F2', 'F3', 'M1', 'V1'}