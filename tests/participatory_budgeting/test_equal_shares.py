from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule_borda import RuleBorda
from whalrus.participatories_budgeting.equal_shares import EqualShares
import copy

def test_approval():


     p = Profile([{"A":1,"B":1,"C":0,"D":0,"E":0},
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

     pb = EqualShares(p, base_rule = RuleApproval(),
          project_cost = {'A':700, 'B':400, 'C':250, 'D':200, 'E':100}, budget = 1100)


     assert pb.winners_ == ['A','D','E']


     p = Profile([{"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":0,"B":0,"C":1,"D":1,"E":1},
                    {"A":0,"B":0,"C":0,"D":1,"E":0},
                    {"A":0,"B":0,"C":0,"D":1,"E":1},
                    {"A":0,"B":0,"C":1,"D":1,"E":1},
                    {"A":0,"B":1,"C":0,"D":0,"E":0}])

     pb = EqualShares(p, base_rule = RuleApproval(),
          project_cost = {'A':700, 'B':400, 'C':250, 'D':200, 'E':100}, budget = 1100)

     assert pb.winners_ == ['B','C','D']

     pb.check
def test_utility():

     p = Profile(['p1 > p2 > p3','p1 > p2 > p3','p3 > p2 > p1'])

     pb = EqualShares(p, base_rule = RuleBorda(), project_cost = {"p1": 100, "p2": 50, "p3": 50}, budget = 150)
     assert pb.winners_ == ['p1','p3']