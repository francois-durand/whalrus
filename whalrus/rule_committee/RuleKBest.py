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
from whalrus.utils.Utils import cached_property, NiceSet, NiceFrozenSet
from whalrus.priority.Priority import Priority
from whalrus.rule_committee.RuleCommittee import RuleCommittee
from whalrus.rule.Rule import Rule
from itertools import combinations


class RuleKBest(RuleCommittee):
    """
    A multi-winner rule that selects the best k candidates of a single winner voting rule.

    :param committee_size: the number of candidates that will be elected in the committee.
    :param base_rule: the single winner voting rule.
    :param use_base_rule_tie_break: if True (default), then the tie-break of the base rule (over the candidates) is
        used to compute a strict order, then the best candidates in this order are elected. In that case,
        no tie-break over the committees is necessary. If False, then the (weak) order of the base rule is used to
        establish the cowinning committees, then the tie-break of RuleKBest (over the committees) is used.

    >>> from whalrus import RulePlurality
    >>> rule = RuleKBest(
    ...     ballots=['a', 'b', 'c', 'd'], weights=[3, 2, 2, 1],
    ...     committee_size=2, base_rule=RulePlurality(tie_break=Priority.ASCENDING))
    >>> rule.winning_committee_
    {'a', 'b'}
    """

    def __init__(self, *args, committee_size: int, base_rule: Rule, use_base_rule_tie_break: bool = True, **kwargs):
        self.committee_size = committee_size
        self.base_rule = base_rule
        self.use_base_rule_tie_break = use_base_rule_tie_break
        super().__init__(*args, **kwargs)

    @cached_property
    def base_rule_(self) -> Rule:
        """
        The base rule.

        :return: the base rule (once computed with the given profile).
        """
        return self.base_rule(ballots=self.profile_converted_, candidates=self.candidates_)

    @cached_property
    def winning_committee_(self) -> NiceSet:
        if self.use_base_rule_tie_break:
            return NiceSet(self.base_rule_.strict_order_[:self.committee_size])
        else:
            return super().winning_committee_

    @cached_property
    def cowinning_committees_(self) -> NiceSet:
        if self.use_base_rule_tie_break:
            return NiceSet({NiceFrozenSet(self.winning_committee_)})
        else:
            base_set = set()
            free_seats = self.committee_size
            for equivalence_class in self.base_rule_.order_:
                len_class = len(equivalence_class)
                if len_class >= free_seats:
                    return NiceSet(NiceFrozenSet(base_set.union(subset))
                                   for subset in combinations(equivalence_class, free_seats))
                base_set.update(equivalence_class)
                free_seats -= len_class

    @cached_property
    def trailing_committee_(self) -> NiceSet:
        if self.use_base_rule_tie_break:
            return NiceSet(self.base_rule_.strict_order_[-self.committee_size:])
        else:
            return super().trailing_committee_

    @cached_property
    def cotrailing_committees_(self) -> NiceSet:
        if self.use_base_rule_tie_break:
            return NiceSet({NiceFrozenSet(self.trailing_committee_)})
        else:
            base_set = set()
            free_seats = self.committee_size
            for equivalence_class in self.base_rule_.order_[::-1]:
                len_class = len(equivalence_class)
                if len_class >= free_seats:
                    return NiceSet(NiceFrozenSet(base_set.union(subset))
                                   for subset in combinations(equivalence_class, free_seats))
                base_set.update(equivalence_class)
                free_seats -= len_class

    @cached_property
    def order_on_committees_(self) -> list:
        raise NotImplementedError
