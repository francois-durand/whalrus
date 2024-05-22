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
from whalrus.rules_committee.rule_committee_scoring import RuleCommitteeScoring
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

class RuleSTV(RuleCommitteeScoring):

    def __init__(self, *args, base_rule: Rule = None, rule: Rule = None, propagate_tie_break=True,
                 **kwargs):
        self.base_rule = base_rule
        if rule is None:
            rule = RulePlurality(tie_break = Priority.ASCENDING,converter = ConverterBallotToPlurality(Priority.ASCENDING))
        self.rule = rule
        self.propagate_tie_break = propagate_tie_break
        super().__init__(*args, **kwargs)

    def stv_(self) -> list:

        elected = []
        quota = np.floor(sum(self.profile_converted_.weights)/(self.committee_size + 1)) + 1
        new_profile = copy.deepcopy(self.profile_converted_)
        self.rule(new_profile)

        while len(elected) < self.committee_size:
        
        
            ballots = []
            weights = []

            score_p = self.rule.gross_scores_
            if score_p[self.rule.winner_] >= quota:
        
                elected.append(self.rule.winner_)
                new_set = self.rule.candidates_ - NiceSet({self.rule.winner_})
                over_count = score_p[self.rule.winner_] - quota
                ratio = Fraction(int(over_count),score_p[self.rule.winner_])
                for ballot, weight, _  in new_profile.items():
        
                    if len(ballot) >= 1 and ballot.first() != self.rule.winner_:
                        ballots.append(ballot.restrict(new_set))
                        weights.append(weight)
                    elif len(ballot) > 1 and ratio > 0:
                        ballots.append(ballot.restrict(new_set))
                        weights.append(weight*ratio)
                        
            else:
                elimination = EliminationLast(rule=self.rule, k=1)
                new_set = elimination.qualified_

                for ballot, weight, _  in new_profile.items():
                    try:
                        ballots.append(ballot.restrict(new_set))
                        weights.append(weight) 
                    except:
                        pass
       
                    
            new_profile = Profile(ballots, weights = weights)

            self.rule(new_profile)
            if len(self.rule.candidates_) + len(elected) == self.committee_size and len(elected) != self.committee_size:
                 
                return NiceFrozenSet(set(elected).union(self.rule.candidates_))

        return NiceFrozenSet(elected)
