from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule_borda import RuleBorda
from whalrus.participatories_budgeting.equal_shares import EqualShares
from whalrus.ballots.ballot_levels import BallotLevels
from whalrus.rules.rule_approval import RuleApproval
from whalrus.scales.scale_from_list import ScaleFromList
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
     

     assert pb.winners_ == {'A','D','E'}
     assert pb.eliminated_ == {'B', 'C'}
     assert pb.remaining_budget_ == 100

     pb(budget = 1500)
     assert pb.budget == 1500
     assert pb.winners_ == {'A', 'C', 'D', 'E'}
     assert pb.eliminated_ == {'B'}
     assert pb.remaining_budget_ == 250


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

     assert pb.winners_ == {'B','C','D'}
     assert pb.eliminated_ == {'A', 'E'}
     assert pb.remaining_budget_ == 250
     
def test_utility():

     p = Profile(['p1 > p2 > p3','p1 > p2 > p3','p3 > p2 > p1'])

     pb = EqualShares(p, base_rule = RuleBorda(), project_cost = {"p1": 100, "p2": 50, "p3": 50}, budget = 150)
     assert pb.winners_ == {'p1','p3'}
     assert pb.eliminated_ == {'p2'}
     assert pb.remaining_budget_ == 0 
     

def test_grades_approval():

     p = Profile([
            BallotLevels({"A":"Excellent","B":"Good","C":"Bad","D":"Bad","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])), 
            BallotLevels({"A":"Excellent","B":"Excellent","C":"Bad","D":"Reject","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Good","B":"Good","C":"Medium","D":"Bad","E":"Bad"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Excellent","B":"Good","C":"Excellent","D":"Bad","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Excellent","B":"Good","C":"Bad","D":"Bad","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Excellent","B":"Excellent","C":"Bad","D":"Reject","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Reject","B":"Reject","C":"Medium","D":"Good","E":"Excellent"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Bad","B":"Bad","C":"Reject","D":"Excellent","E":"Bad"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Reject","B":"Bad","C":"Bad","D":"Excellent","E":"Good"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Reject","B":"Reject","C":"Medium","D":"Good","E":"Excellent"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),                  
            BallotLevels({"A":"Excellent","B":"Reject","C":"Bad","D":"Reject","E":"Bad"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent']))
      ])

     pb = EqualShares(p, base_rule = RuleApproval(),
          project_cost = {'A':700, 'B':400, 'C':250, 'D':200, 'E':100}, budget = 1100)

     assert pb.winners_ == {'A', 'D', 'E'}
     assert pb.eliminated_ == {'B', 'C'}
     assert pb.remaining_budget_ == 100     

def test_grades_borda():

 
     
     p = Profile([
            BallotLevels({"A":"Excellent","B":"Good","C":"Bad","D":"Bad","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])), 
            BallotLevels({"A":"Excellent","B":"Excellent","C":"Bad","D":"Reject","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Good","B":"Good","C":"Medium","D":"Bad","E":"Bad"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Excellent","B":"Good","C":"Excellent","D":"Bad","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Excellent","B":"Good","C":"Bad","D":"Bad","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Excellent","B":"Excellent","C":"Bad","D":"Reject","E":"Reject"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Reject","B":"Reject","C":"Medium","D":"Good","E":"Excellent"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Bad","B":"Bad","C":"Reject","D":"Excellent","E":"Bad"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Reject","B":"Bad","C":"Bad","D":"Excellent","E":"Good"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),
            BallotLevels({"A":"Reject","B":"Reject","C":"Medium","D":"Good","E":"Excellent"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent'])),                  
            BallotLevels({"A":"Excellent","B":"Reject","C":"Bad","D":"Reject","E":"Bad"},scale = ScaleFromList(['Reject','Bad', 'Medium','Good','Excellent']))
      ])

     pb = EqualShares(p, base_rule = RuleBorda(),
          project_cost = {'A':700, 'B':400, 'C':250, 'D':200, 'E':100}, budget = 1100)

     assert pb.winners_ == {'A', 'D', 'E'}
     assert pb.eliminated_ == {'B', 'C'}
     assert pb.remaining_budget_ == 100   
