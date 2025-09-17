from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule_borda import RuleBorda
from whalrus.participatories_budgeting.mes_utilitarian_completion import MesUtilitarianCompletion
import copy


def test():

    p = Profile([{"p1": 1, "p2": 1, "p3":0}, {"p1": 1, "p2": 0, "p3":0}, {"p1": 0, "p2": 0, "p3":1}])

    mes = MesUtilitarianCompletion(p, project_cost = {"p1": 100, "p2": 50, "p3": 50}, budget = 150, base_rule = RuleApproval())
    
    assert mes.completed_winners_ == {'p1', 'p3'}

def test_uncompleted():

    p = Profile([
        {'Chicken':0, 'Cheese': 0 , 'Pie': 0, 'Cake': 1, 'Gaspacho': 0, 'Salad': 1},
        {'Chicken':0, 'Cheese': 1 , 'Pie': 1, 'Cake': 1, 'Gaspacho': 1, 'Salad': 0},
        {'Chicken':0, 'Cheese': 1 , 'Pie': 0, 'Cake': 1, 'Gaspacho': 0, 'Salad': 0},
        {'Chicken':0, 'Cheese': 1 , 'Pie': 1, 'Cake': 0, 'Gaspacho': 1, 'Salad': 1},
        {'Chicken':0, 'Cheese': 0 , 'Pie': 1, 'Cake': 1, 'Gaspacho': 1, 'Salad': 1},
        {'Chicken':0, 'Cheese': 1 , 'Pie': 1, 'Cake': 0, 'Gaspacho': 1, 'Salad': 1},
        {'Chicken':0, 'Cheese': 1 , 'Pie': 0, 'Cake': 0, 'Gaspacho': 1, 'Salad': 1},
        {'Chicken':0, 'Cheese': 0 , 'Pie': 0, 'Cake': 1, 'Gaspacho': 1, 'Salad': 1},
        {'Chicken':0, 'Cheese': 0 , 'Pie': 0, 'Cake': 0, 'Gaspacho': 0, 'Salad': 1},
        {'Chicken':1, 'Cheese': 1 , 'Pie': 0, 'Cake': 0, 'Gaspacho': 0, 'Salad': 1},
        {'Chicken':1, 'Cheese': 1 , 'Pie': 0, 'Cake': 1, 'Gaspacho': 0, 'Salad': 1},
        {'Chicken':0, 'Cheese': 1 , 'Pie': 1, 'Cake': 1, 'Gaspacho': 0, 'Salad': 0}
    ])

    project_cost = {'Chicken':25, 'Cheese': 30, 'Pie': 15, 'Cake': 15, 'Gaspacho': 10, 'Salad': 20}

    mes = MesUtilitarianCompletion(p, project_cost = project_cost, budget = 60, base_rule = RuleApproval())
    assert mes.completed_winners_ == {'Cake', 'Gaspacho', 'Pie', 'Salad'}