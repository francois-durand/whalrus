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
from whalrus.utils.Utils import cached_property, NiceSet
from whalrus.rule.Rule import Rule
from whalrus.rule.RulePlurality import RulePlurality
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.priority.Priority import Priority


class RuleSequentialTieBreak(Rule):
    """
    A rule by sequential tie-break.

    :param `*args`: cf. parent class.
    :param rules: a list of rules.
    :param `**kwargs`: cf. parent class.

    The winner is determined by the first rule. If there is a tie, it is broken by the second rule. Etc. There may
    still be a tie at the end: in that case, it is broken by the tie-breaking rule of this object.

    >>> rule = RuleSequentialTieBreak(
    ...     ['a > d > e > b > c', 'b > d > e > a > c', 'c > d > e > a > b',
    ...      'd > e > b > a > c', 'e > d > b > a > c'],
    ...     weights=[2, 2, 2, 1, 1],
    ...     rules=[RulePlurality(), RuleBorda()], tie_break=Priority.ASCENDING)
    >>> rule.rules_[0].gross_scores_
    {'a': 2, 'b': 2, 'c': 2, 'd': 1, 'e': 1}
    >>> rule.rules_[1].gross_scores_
    {'a': 14, 'b': 14, 'c': 8, 'd': 25, 'e': 19}
    >>> rule.order_
    [{'a', 'b'}, {'c'}, {'d'}, {'e'}]
    >>> rule.winner_
    'a'
    """

    def __init__(self, *args, rules: list = None, **kwargs):
        self.rules = rules
        super().__init__(*args, **kwargs)

    @cached_property
    def rules_(self) -> list:
        """
        The rules (once applied to the profile).

        :return: a list of :class:`Rule` objects (once applied to the profile).
        """
        return [rule(self.profile_converted_) for rule in self.rules]

    @cached_property
    def order_(self) -> list:
        orders = [rule.order_ for rule in self.rules_]
        # rank_tuples[a] will be (rank in order 0, rank in order 1, ...)
        rank_tuples = {c: [] for c in self.candidates_}
        for order in orders:
            for i, tie_class in enumerate(order):
                for c in tie_class:
                    rank_tuples[c].append(i)
        rank_tuples = {k: tuple(v) for k, v in rank_tuples.items()}
        # Now, sort by lexicographic order of "rank tuples"
        return [NiceSet(k for k in rank_tuples.keys() if rank_tuples[k] == v)
                for v in sorted(set(rank_tuples.values()))]

    # TODO: some methods such as cowinners_ might be overridden for a better performance.
