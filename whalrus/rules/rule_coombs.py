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
from whalrus.rules.rule import Rule
from whalrus.rules.rule_iterated_elimination import RuleIteratedElimination
from whalrus.rules.rule_veto import RuleVeto
from whalrus.eliminations.elimination import Elimination
from whalrus.eliminations.elimination_last import EliminationLast


class RuleCoombs(RuleIteratedElimination):
    """
    Coombs' rule.

    Parameters
    ----------
    args
        Cf. parent class.
    base_rule : Rule
        Default: :class:`RuleVeto`.
    elimination : Elimination
        Default: :class:`EliminationLast` with ``k=1``.
    kwargs
        Cf. parent class.

    Examples
    --------
    At each round, the candidate with the worst Veto score is eliminated.

        >>> rule = RuleCoombs(['a > b > c', 'b > a > c', 'c > a > b'], weights=[2, 3, 4])
        >>> rule.eliminations_[0].rule_.gross_scores_
        {'a': 0, 'b': -4, 'c': -5}
        >>> rule.eliminations_[1].rule_.gross_scores_
        {'a': -3, 'b': -6}
        >>> rule.eliminations_[2].rule_.gross_scores_
        {'a': -9}
        >>> rule.winner_
        'a'
    """

    def __init__(self, *args, base_rule: Rule = None, elimination: Elimination = None, **kwargs):
        if base_rule is None:
            base_rule = RuleVeto()
        if elimination is None:
            elimination = EliminationLast(k=1)
        super().__init__(*args, base_rule=base_rule, elimination=elimination, **kwargs)
