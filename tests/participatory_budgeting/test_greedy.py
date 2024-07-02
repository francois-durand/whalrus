from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule_borda import RuleBorda
from whalrus.participatories_budgeting.greedy import Greedy
import copy

def test():

    p = Profile([   {"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":0,"B":0,"C":1,"D":1,"E":1},
                    {"A":0,"B":0,"C":0,"D":1,"E":0},
                    {"A":0,"B":0,"C":0,"D":1,"E":1},
                    {"A":0,"B":0,"C":1,"D":1,"E":1},
                    {"A":1,"B":0,"C":0,"D":0,"E":0}])
    
    pb = Greedy(p, base_rule = RuleApproval(),
          project_cost = {'A':700, 'B':400, 'C':250, 'D':200, 'E':100}, budget = 1100)

    assert pb.winners_ == {'A', 'B'}
    

    p = Profile([   {"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":0,"B":0,"C":1,"D":1,"E":1},
                    {"A":0,"B":0,"C":0,"D":1,"E":0},
                    {"A":0,"B":0,"C":0,"D":1,"E":1},
                    {"A":0,"B":0,"C":1,"D":1,"E":1},
                    {"A":1,"B":0,"C":0,"D":0,"E":0}])
    
    pb = Greedy(p, base_rule = RuleApproval(),
          project_cost = {'A':700, 'B':400, 'C':250, 'D':200, 'E':100}, budget = 1100)

    assert pb.winners_ == {'A', 'C', 'E'}

    