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
from whalrus.utils.utils import cached_property
from whalrus.rules.rule import Rule
from whalrus.rules.rule_borda import RuleBorda
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.rules.rule_sequential_elimination import RuleSequentialElimination
from whalrus.eliminations.elimination import Elimination
from whalrus.eliminations.elimination_last import EliminationLast


class RuleTwoRound(RuleSequentialElimination):
    # noinspection PyUnresolvedReferences
    """
    The two-round system.

    Parameters
    ----------
    args
        Cf. parent class.
    rule1
        The first rule. Default: :class:`RulePlurality`.
    rule2
        The second rule. Default: :class:`RulePlurality`.
    elimination : Elimination
        The elimination algorithm used during the first round. Default: :class:`EliminationLast` with ``k=-2``, which
        only keeps the 2 best candidates.
    kwargs
        Cf. parent class.

    Examples
    --------
    With its default settings, this class implements the classic two-round system, using plurality at both rounds:

        >>> rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'],
        ...                     weights=[2, 2, 1])
        >>> rule.first_round_.rule_.gross_scores_
        {'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 0}
        >>> rule.second_round_.gross_scores_
        {'a': 3, 'b': 2}

    Using the options, some more exotic two-round systems can be defined, such as changing the rule of a round:

        >>> rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'],
        ...                     weights=[2, 2, 1], rule1=RuleBorda())
        >>> rule.first_round_.rule_.gross_scores_
        {'a': 17, 'b': 16, 'c': 12, 'd': 5, 'e': 0}
        >>> rule.second_round_.gross_scores_
        {'a': 3, 'b': 2}

    ... or changing the elimination algorithm:

        >>> rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'],
        ...                     weights=[2, 2, 1], elimination=EliminationLast(k=-3))
        >>> rule.first_round_.rule_.gross_scores_
        {'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 0}
        >>> rule.second_round_.gross_scores_
        {'a': 2, 'b': 2, 'c': 1}
    """

    def __init__(self, *args, rule1: Rule = None, rule2: Rule = None, elimination: Elimination = None, **kwargs):
        if rule1 is None:
            rule1 = RulePlurality()
        if rule2 is None:
            rule2 = RulePlurality()
        if elimination is None:
            elimination = EliminationLast(k=-2)
        super().__init__(*args, rules=[rule1, rule2], eliminations=[elimination], **kwargs)

    @cached_property
    def first_round_(self) -> Elimination:
        """Elimination: The first round. This is just a shortcut for ``self.elimination_rounds_[0]``.
        """
        return self.elimination_rounds_[0]

    @cached_property
    def second_round_(self) -> Rule:
        """Rule: The second round. This is just an alternative name for ``self.final_round_``.
        """
        return self.final_round_
