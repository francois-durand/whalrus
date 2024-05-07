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
from whalrus.utils.utils import cached_property, NiceSet, NiceFrozenSet, NiceDict
from whalrus.priorities.priority import Priority
from whalrus.priorities.priority_lifted_leximax import PriorityLiftedLeximax
from whalrus.rules_committee.rule_committee import RuleCommittee
from itertools import combinations


class RuleCommitteeScoring(RuleCommittee):
    # noinspection PyUnresolvedReferences
    """
    A multi-winner rule that select the best committee according to a Committee Scoring voting rule.

    :param committee_size: the number of candidates that will be elected in the committee.
    :param committee_legality_function: a function that maps a committee to a Boolean, indicating whether the committee
        is authorized or not. This can be used, for example, to ensure gender balance (cf. example below).

    Each possible committee is assigned a score in the following way: each voter gives the committee a number of points
    which is defined in the :function:`_cc_scores` method. This method should be implemented in concrete subclasses.

    Cf. :class:`RuleChamberlinCourant` for some examples.
    """

    def __init__(self, *args, committee_size: int = None,
                 committee_legality_function=None, **kwargs):
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
        raise NotImplementedError

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The scores of all committees.

        :return: a :class:`NiceDict` that, to each committee, associates its score.
        """
        return NiceDict({committee: self._cc_score(committee) for committee in self._all_committees()})

    @cached_property
    def order_on_committees_(self) -> list:
        return [NiceSet(committee for committee in self.scores_.keys() if self.scores_[committee] == v)
                for v in sorted(set(self.scores_.values()), reverse=True)]
