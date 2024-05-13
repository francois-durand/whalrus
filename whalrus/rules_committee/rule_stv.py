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

from whalrus.rules_committee.rule_committee_scoring import RuleCommitteeScoring
from whalrus.converters_ballot.converter_ballot_to_plurality import ConverterBallotToPlurality
from whalrus.scorers.scorer_plurality import ScorerPlurality
from whalrus.eliminations.elimination_last import EliminationLast, Elimination
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.scorers.scorer_plurality import ScorerPlurality
from whalrus.priorities.priority import Priority 
from whalrus.rules.rule import Rule
from whalrus.utils.utils import cached_property, NiceSet
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

    def transfert_(self):
        pass

    #@cached_property
    def rounds_(self) -> list:

        elected = []
        l_eliminated = []
        quota = np.ceil(len(self.profile_converted_.voters)/self.committee_size)

        new_profile = copy.deepcopy(self.profile_converted_)
        plurality = RulePlurality(tie_break=Priority.ASCENDING)
        plurality(new_profile)
        
        while len(elected) < self.committee_size:
      
            
            score_p = plurality.gross_scores_
            if score_p[plurality.winner_] >= quota:
               
                elected.append(plurality.winner_)
                
                new_set = plurality.candidates_ - NiceSet(plurality.winner_)
                ballots = []
                for i in range(int(quota), score_p[plurality.winner_] + 1):
                    rand_ballot = random.choice(new_profile)
                    ballots.append(rand_ballot.restrict(new_set))
                    new_profile.remove(rand_ballot)
                    
                for ballot in new_profile:
                    if ballot.first() == plurality.winner_:
                        new_profile.remove(ballot)

                for ballot in new_profile:
                    ballots.append(ballot.restrict(new_set))
            
            else:
                elimination = EliminationLast(rule=plurality, k=1)
                new_set = elimination.qualified_
                ballots = []
               
                for ballot in new_profile:
            
                    ballots.append(ballot.restrict(new_set))
                    
                
            new_profile = Profile(ballots)
            plurality = RulePlurality(tie_break=Priority.ASCENDING)
            plurality(new_profile)

            if len(plurality.candidates_) + len(elected) == self.committee_size:
                return plurality.candidates_

        return elected


    def _cc_score(self, committee):
        converter = ConverterBallotToPlurality()
        scorer = ScorerPlurality()

        return sum(
            sum(
                scorer(ballot=converter(ballot), candidates=self.candidates_).scores_[candidate]
                for candidate in committee
            )
            for ballot in self.profile_converted_
        )
    
        
#rule = RuleSTV(['c > b > a', 'b> c > a', 'b > c > a'], committee_size = 1)
rule = RuleSTV(['f > e > d > b > c > a', 'f > e > d > b > c > a',
      'f > e > d > b > c > a' ,'f > e > d > b > c > a',
       'a > b > c > d > e > f','a > b > c > d > e > f',
       'a > b > c > d > e > f',
       'b > c > a > e > d > f', 'b > c > a > e > d > f'
       , 'd > c > a > b > e > f'], committee_size = 2)

print(rule.rounds_())