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
from whalrus.rules.rule_condorcet import RuleCondorcet
from whalrus.rules.rule_borda import RuleBorda
from whalrus.rules.rule_sequential_tie_break import RuleSequentialTieBreak


class RuleBlack(RuleSequentialTieBreak):
    """
    Black's rule.

    Parameters
    ----------
    args
        Cf. parent class.
    rule_condorcet : Rule
        Used as the main victory criterion. Default: :class:`RuleCondorcet`.
    rule_borda : Rule
        Used as the secondary victory criterion. Default: :class:`RuleBorda`.
    kwargs
        Cf. parent class.

    Examples
    --------
    As a main victory criterion, the Condorcet winner is elected (even if it does not have the highest Borda score):

        >>> rule = RuleBlack(ballots=['a > b > c', 'b > c > a'], weights=[3, 2])
        >>> rule.rule_condorcet_.matrix_majority_.matrix_weighted_majority_.as_array_
        array([[0, Fraction(3, 5), Fraction(3, 5)],
               [Fraction(2, 5), 0, 1],
               [Fraction(2, 5), 0, 0]], dtype=object)
        >>> rule.order_
        [{'a'}, {'b'}, {'c'}]

    When there is no Condorcet winner, candidates are sorted according to their Borda scores:

        >>> rule = RuleBlack(ballots=['a > b > c', 'b > c > a', 'c > a > b'], weights=[3, 2, 2])
        >>> rule.rule_condorcet_.matrix_majority_.matrix_weighted_majority_.as_array_
        array([[0, Fraction(5, 7), Fraction(3, 7)],
               [Fraction(2, 7), 0, Fraction(5, 7)],
               [Fraction(4, 7), Fraction(2, 7), 0]], dtype=object)
        >>> rule.order_
        [{'a'}, {'b'}, {'c'}]
    """

    def __init__(self, *args, rule_condorcet: Rule = None, rule_borda: Rule = None, **kwargs):
        if rule_condorcet is None:
            rule_condorcet = RuleCondorcet()
        self.rule_condorcet = rule_condorcet
        if rule_borda is None:
            rule_borda = RuleBorda()
        self.rule_borda = rule_borda
        super().__init__(*args, rules=[rule_condorcet, rule_borda], **kwargs)

    @cached_property
    def rule_condorcet_(self):
        """Rule: The Condorcet rule (once applied to the profile).

        Examples
        --------
            >>> rule = RuleBlack(ballots=['a > b > c', 'b > c > a'], weights=[3, 2])
            >>> rule.rule_condorcet_.matrix_majority_.as_array_
            array([[Fraction(1, 2), 1, 1],
                   [0, Fraction(1, 2), 1],
                   [0, 0, Fraction(1, 2)]], dtype=object)
        """
        return self.rules_[0]

    @cached_property
    def rule_borda_(self):
        """Rule: The Borda rule (once applied to the profile).

        Examples
        --------
            >>> rule = RuleBlack(ballots=['a > b > c', 'b > c > a'], weights=[3, 2])
            >>> rule.rule_borda_.scores_
            {'a': Fraction(6, 5), 'b': Fraction(7, 5), 'c': Fraction(2, 5)}
        """
        return self.rules_[1]
