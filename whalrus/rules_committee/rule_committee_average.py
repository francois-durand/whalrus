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
from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.scorers.scorer import Scorer
from itertools import combinations

    
    
class RuleCommitteeAverage(RuleCommittee):
    """
    Based on RuleCommitteeScoring, with the possibility to also have
    normalized scores (useful in the case of incomplete ballots).
    
    """

    def __init__(self, *args, committee_size: int = None,
                 committee_legality_function=None, base_rule = None, **kwargs):
        self.base_rule = base_rule
    
        if committee_legality_function is None:
            # noinspection PyUnusedLocal
            def committee_legality_function(committee):
                return True
        # Parameters
        self.committee_size = committee_size
        self.committee_legality_function = committee_legality_function
        super().__init__(*args, **kwargs)

    def _all_committees(self):
        if self.committee_size is None:
            possible_sizes = range(1, self.n_candidates_ + 1)
        else:
            possible_sizes = [self.committee_size]
        yield from (NiceFrozenSet(s)
                    for k in possible_sizes for s in combinations(self.candidates_, k)
                    if self.committee_legality_function(s))

    def _cc_score(self, committee):
        return sum(
                self.base_rule_.scores_[candidate] for candidate in committee
        )

    def _cc_gross_scores(self, committee):
        return sum(
                self.base_rule_.gross_scores_[candidate] for candidate in committee
        )

    @cached_property
    def base_rule_(self):
        return self.base_rule(ballots = self.profile_converted_, candidates = self.candidates_)

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The normalized scores of all committees.

        :return: a :class:`NiceDict` that, to each committee, associates its score.
        """
        return NiceDict({committee: self._cc_score(committee) for committee in self._all_committees()})

    @cached_property
    def gross_scores_(self) -> NiceDict:
        """
        The gross scores of all committees.

        :return: a :class:`NiceDict` that, to each committee, associates its score.
        """
        return NiceDict({committee: self._cc_gross_scores(committee) for committee in self._all_committees()})
    

    @cached_property
    def order_on_committees_(self) -> list:
        return [NiceSet(committee for committee in self.scores_.keys() if self.scores_[committee] == v)
                for v in sorted(set(self.scores_.values()), reverse=True)]