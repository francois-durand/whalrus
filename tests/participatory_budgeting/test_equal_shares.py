from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.participatories_budgeting.equal_shares import EqualShares
import copy

def test():

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
    
    r = copy.deepcopy(pb.initial_vote_counts)
    print(r)
    del r["A"]
    print(r)
    #print(pb.shares_)