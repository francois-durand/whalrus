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
from whalrus.utils.utils import cached_property
import numpy as np

class RuleSTV(RuleCommitteeScoring):

    def __init__(self, *args, base_rule: Rule = None, elimination: Elimination = None, propagate_tie_break=True,
                 **kwargs):
        if elimination is None:
            elimination = EliminationLast(k=1)
        self.base_rule = base_rule
        self.elimination = elimination
        self.propagate_tie_break = propagate_tie_break
        super().__init__(*args, **kwargs)

    #@cached_property
    def rounds_(self) -> list:

        elected = []
        quota = np.ceil(len(self.candidates_)/self.committee_size)

        plurality = RulePlurality(tie_break=Priority.ASCENDING)
        plurality(self.profile_converted_)
        
        if plurality.gross_scores_[plurality.winner_] >= quota:
            elected.append(plurality.winner_)

          
     
        
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
    
        
rule = RuleSTV(['a > b > c', 'a > c > b', 'b > a > c'], committee_size = 2)

print(rule.rounds_())