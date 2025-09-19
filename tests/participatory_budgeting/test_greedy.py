from whalrus.profiles.profile import Profile
from whalrus.rules.rule_approval import RuleApproval
from whalrus.rules.rule_borda import RuleBorda
from whalrus.rules.rule_majority_judgment import RuleMajorityJudgment
from whalrus.scales.scale_from_list import ScaleFromList
from whalrus.participatories_budgeting.greedy import Greedy
from whalrus.ballots.ballot_levels import BallotLevels
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
    assert pb.eliminated_ == {'C','D','E'}
    assert pb.remaining_budget_ == 0
    

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
    assert pb.eliminated_ == {'B','D'}
    assert pb.remaining_budget_ == 50

def test_grades():

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

      pb = Greedy(p, base_rule = RuleMajorityJudgment(),
          project_cost = {'A':700, 'B':400, 'C':250, 'D':200, 'E':100}, budget = 1100)

      assert pb.winners_ == {"A","B"} 
      assert pb.eliminated_ == {'C','D','E'}     
      assert pb.remaining_budget_ == 0

def test_tie_break():
      p = Profile([   {"A":1,"B":1,"C":0,"D":1,"E":0},
                    {"A":1,"B":1,"C":1,"D":1,"E":0},
                    {"A":1,"B":1,"C":1,"D":0,"E":0},
                    {"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":1,"B":1,"C":0,"D":1,"E":0},
                    {"A":1,"B":1,"C":0,"D":0,"E":0},
                    {"A":0,"B":0,"C":0,"D":1,"E":1},
                    {"A":0,"B":0,"C":0,"D":1,"E":0},
                    {"A":0,"B":0,"C":0,"D":1,"E":1},
                    {"A":0,"B":1,"C":1,"D":0,"E":1},
                    {"A":1,"B":0,"C":0,"D":1,"E":0}])
    
      pb = Greedy(p, base_rule = RuleApproval(),
          project_cost = {'A':700, 'B':400, 'C':250, 'D':200, 'E':100}, budget = 1100)

      assert pb.base_rule_.order_ == [{'A', 'B', 'D'}, {'C', 'E'}]
      assert pb.winners_ == {'D', 'B', 'E', 'C'}
      assert pb.eliminated_ == {'A'}
      assert pb.remaining_budget_ == 150