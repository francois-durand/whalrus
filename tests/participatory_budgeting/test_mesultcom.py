from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule_borda import RuleBorda
from whalrus.participatories_budgeting.mes_utilitarian_completion import MesUtilitarianCompletion
import copy


def test():

    p = Profile([{"p1": 1, "p2": 1, "p3":0}, {"p1": 1, "p2": 0, "p3":0}, {"p1": 0, "p2": 0, "p3":1}])

    mes = MesUtilitarianCompletion(p, project_cost = {"p1": 100, "p2": 50, "p3": 50}, budget = 150, base_rule = RuleApproval())
    
    assert mes.completed_winners_ == {'p1', 'p3'}