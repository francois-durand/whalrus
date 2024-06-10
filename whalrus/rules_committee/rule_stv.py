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
from fractions import Fraction
from whalrus.rules_committee.rule_transfert import RuleTransfert
from whalrus.converters_ballot.converter_ballot_to_plurality import ConverterBallotToPlurality
from whalrus.scorers.scorer_plurality import ScorerPlurality
from whalrus.eliminations.elimination_last import EliminationLast, Elimination
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.scorers.scorer_plurality import ScorerPlurality
from whalrus.priorities.priority import Priority 
from whalrus.rules.rule import Rule
from whalrus.utils.utils import cached_property, NiceSet, NiceFrozenSet, NiceDict
from whalrus.profiles.profile import Profile
import numpy as np
import random
import copy

from pprint import pprint

# import inspect module
import inspect

class RuleSTV(RuleTransfert):

    """
    A multi-winner rule that select the best committee according using transferable votes.

    -----------

    A quota q is calculated as q = floor(n/k+1) + 1 where n is the number of voters and k the size of the committee to be elected.
    At each round, we check if the plurality winner score is greater than the quota:
        If it's the case, we transfer the surplus to each possible second choice according to their proportion in the whole set of ballots
        where the winner is in first choice.
    If not:
        We eliminate the lowest plurality candidate.
    We perform rounds until the remaining candidates (included thoses elected) reaches the size of the committee
    
    """

    def __init__(self, *args, committee_size: int, base_rule: Rule = None, rule: Rule = None, propagate_tie_break=True, quota = False,
                 **kwargs):
        self.base_rule = base_rule
        self.committee_size = committee_size
        if rule is None:
            rule = RulePlurality(tie_break = Priority.ASCENDING,converter = ConverterBallotToPlurality(Priority.ASCENDING))
        self.rule = rule
        self.propagate_tie_break = propagate_tie_break
        super().__init__(*args, ** kwargs)
        if quota:
            self.quota = np.floor(sum(self.profile_converted_.weights)/(self.committee_size + 1 )) + 1
        else:
            self.quota = np.floor(sum(self.profile_converted_.weights)/self.committee_size)

    @cached_property
    def transfert_(self) -> list:
        elected = dict()
        eliminated = {}
        rule = copy.deepcopy(self.rule)
        new_profile = copy.deepcopy(self.profile_converted_)
        new_set = self.candidates_
        rule(new_profile)
        rounds = [(rule,elected.copy(),eliminated.copy())]
    
        while len(elected) < self.committee_size:
        
            ballots = []
            weights = []

            score_p = rule.gross_scores_
  
            if score_p[rule.winner_] >= self.quota:
                
                elected[rule.winner_] = score_p[rule.winner_]
                new_set_ = new_set - NiceSet({rule.winner_})
                over_count = score_p[rule.winner_] - self.quota
                ratio = Fraction(int(over_count),score_p[rule.winner_])
                for ballot, weight, _  in new_profile.items():
               
                    ballot = ballot.restrict(new_set)

                    if len(ballot) >= 1 and ballot.first() != rule.winner_:
                        ballots.append(ballot.restrict(new_set_))
                        weights.append(weight)
                         
                    elif len(ballot) > 1 and ratio > 0:
                        ballots.append(ballot.restrict(new_set_))
                        weights.append(weight*ratio)
            
                new_profile = Profile(ballots, weights = weights)
                new_set = new_set_
            else:
                elimination = EliminationLast(rule=rule, k=1)
                new_set = elimination.qualified_
                
                e = next(iter(elimination.eliminated_))
   
                eliminated[e] = score_p[e]
            rule(new_profile, candidates=new_set)

            rounds.append((rule, elected.copy(), eliminated.copy()))
         
            if len(rule.candidates_) + len(elected) == self.committee_size:
                for candidate in rule.candidates_:
                    elected[candidate] = score_p[candidate]
                rounds[-1] = (rule, elected, eliminated)
                return rounds
        return rounds


