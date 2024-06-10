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
from whalrus.utils.utils import cached_property, NiceSet, NiceFrozenSet, NiceDict, my_division
from whalrus.priorities.priority import Priority
from whalrus.priorities.priority_lifted_leximax import PriorityLiftedLeximax
from whalrus.rules_committee.rule_committee_scoring import RuleCommitteeScoring
from whalrus.scorers.scorer import Scorer
from itertools import combinations

    
    
class RuleCommitteeAverage(RuleCommitteeScoring):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    
    
    @cached_property
    def _gross_scores_and_weights_(self) -> dict:
        gross_scores = NiceDict({c: 0 for c in self.candidates_})
        weights = NiceDict({c: 0 for c in self.candidates_})
        for ballot, weight, voter in self.profile_converted_.items():
            
            for c, value in self.scorer(ballot=self.converter(ballot), voter=voter, candidates=self.candidates_).scores_.items():
                gross_scores[c] += weight * value
                weights[c] += weight
        return {'gross_scores': gross_scores, 'weights': weights}

    @cached_property
    def weights_(self) -> NiceDict:
        """NiceDict: The weights used for the candidates. For each candidate, this dictionary gives the total weight
        for this candidate, i.e. the total weight of all voters who assign a score to this candidate. This is the
        denominator in the candidate's average score.
        """
        return self._gross_scores_and_weights_['weights']
    
    @cached_property
    def gross_scores(self) -> NiceDict:
        """NiceDict: The gross scores of the candidates. For each candidate, this dictionary gives the sum of its
        scores, multiplied by the weights of the corresponding voters. This is the numerator in the candidate's average
        score.
        """
        return self._gross_scores_and_weights_['gross_scores']

    @cached_property
    def scores(self) -> NiceDict:
        self.default_average = 0
        return NiceDict({c: my_division(score, self.weights_[c], divide_by_zero=self.default_average)
                         for c, score in self.gross_scores.items()})

    def _cc_score(self, committee):
        return sum(
                self.scores[candidate] for candidate in committee
        )

    def _cc_gross_scores(self, committee):
        return sum(
                self.gross_scores[candidate] for candidate in committee
        )
