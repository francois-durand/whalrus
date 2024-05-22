# -*- coding: utf-8 -*-
"""
Copyright Sylvain Bouveret, Yann Chevaleyre and François Durand
sylvain.bouveret@imag.fr, yann.chevaleyre@dauphine.fr, fradurand@gmail.com

This file is part of Whalrus.

Whalrus is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Whalrus is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Whalrus.  If not, see <http://www.gnu.org/licenses/>.
"""
from whalrus.ballots.ballot_order import BallotOrder
from whalrus.rules_committee.rule_committee_scoring import RuleCommitteeScoring
from whalrus.converters_ballot.converter_ballot_to_plurality import ConverterBallotToPlurality
from whalrus.scorers.scorer_plurality import ScorerPlurality
from whalrus.eliminations.elimination_last import EliminationLast, Elimination
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.scorers.scorer_plurality import ScorerPlurality
from whalrus.priorities.priority import Priority 
from whalrus.rules.rule import Rule
from whalrus.utils.utils import cached_property, NiceSet, NiceFrozenSet
from whalrus.profiles.profile import Profile
import numpy as np
import random
import copy

class RuleSTV(RuleCommitteeScoring):

    def __init__(self, *args, base_rule: Rule = None, elimination: Elimination = None, propagate_tie_break=True,
                 **kwargs):
        if elimination is None:
            elimination = EliminationLast(k=1)
        self.base_rule = base_rule
        self.elimination = elimination
        self.propagate_tie_break = propagate_tie_break
        super().__init__(*args, **kwargs)

    
    def stv_(self) -> list:
        converter = ConverterBallotToPlurality(Priority.ASCENDING)
        elected = []
        quota = np.floor(sum(self.profile_converted_.weights)/(self.committee_size + 1)) + 1
        new_profile = copy.deepcopy(self.profile_converted_)
        plurality = RulePlurality(tie_break=Priority.ASCENDING, converter = converter)
        plurality(new_profile)
        
       
        while len(elected) < self.committee_size:
            ballots = []
            w = []

            score_p = plurality.gross_scores_
            if score_p[plurality.winner_] >= quota:
                
                elected.append(plurality.winner_)
                new_set = plurality.candidates_ - NiceSet({plurality.winner_})
                over_count = score_p[plurality.winner_] - quota

                cpt = 0 
                for i in range(len(new_profile)):
                    if(len(new_profile[i]) != 0):
                        if cpt < over_count and new_profile[i].first() == plurality.winner_ and len(new_profile) > 1:
                                ballots.append(new_profile[i].restrict(new_set))
                                if new_profile.weights[i] >= over_count:
                                    w.append(over_count)
                                    cpt += over_count
                                else:
                                    cpt += new_profile.weights[i]
                                    w.append(new_profile.weights[i])
                        
                        elif new_profile[i].first() != plurality.winner_:
                            ballots.append(new_profile[i].restrict(new_set))
                            w.append(new_profile.weights[i])
                        else:
                            pass
                  
          
            else:
                elimination = EliminationLast(rule=plurality, k=1)
                new_set = elimination.qualified_
                for i in range(len(new_profile)):
                    try:
                        ballots.append(new_profile[i].restrict(new_set))
                        w.append(new_profile.weights[i])
                    except:
                        continue 

            new_profile = Profile(ballots, weights = w)
            
            print(new_profile, new_profile.weights)
            plurality(new_profile)
            
            
            if len(plurality.candidates_) + len(elected) == self.committee_size and len(elected) != self.committee_size:
                 
                return NiceFrozenSet(set(elected).union(plurality.candidates_))

        return NiceFrozenSet(elected)


    
        


candidates = {'Oranges','Pears', 'Strawberries', 'Cake', 'Chocolate', 'Hamburgers', 'Chicken'}
b1 = BallotOrder(['Oranges', 'Pears'], candidates = candidates)
b2 = BallotOrder(['Pears','Strawberries', 'Cake'], candidates = candidates)
b3 = BallotOrder(['Strawberries', 'Oranges',' Pears'], candidates = candidates)
b4 = BallotOrder(['Cake','Chocolate'], candidates = candidates)
b5 = BallotOrder(['Chocolate','Cake', 'Hamburgers'], candidates = candidates)
b6 = BallotOrder(['Hamburgers','Chicken'], candidates = candidates)
b7 = BallotOrder(['Chicken','Chocolate', 'Hamburgers'], candidates = candidates)
b8 = BallotOrder(['Pears'], candidates = candidates)

w = [3,8,1,3,1,4,3]

p2 = Profile(ballots = [b1,b2,b3,b4,b5, b6,b7], weights = w)

rule = RuleSTV(p2, committee_size = 2)

print(rule.stv_()) 
