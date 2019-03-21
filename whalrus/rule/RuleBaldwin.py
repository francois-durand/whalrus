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
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.priority.Priority import Priority
from whalrus.rule.Rule import Rule
from whalrus.rule.RuleIteratedElimination import RuleIteratedElimination
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.elimination.Elimination import Elimination
from whalrus.elimination.EliminationLast import EliminationLast
from typing import Union


class RuleBaldwin(RuleIteratedElimination):
    """
    Baldwin's rule.

    :param base_rule: the default is :class:`RuleBorda`.
    :param elimination: the default is :class:`EliminationLast` with ``k=1``.

    At each round, the candidate with the lowest Borda score is eliminated.

    >>> rule = RuleBaldwin(['a > b > c', 'a > b ~ c'])
    >>> rule.eliminations_[0].rule_.gross_scores_
    {'a': 4, 'b': Fraction(3, 2), 'c': Fraction(1, 2)}
    >>> rule.eliminations_[1].rule_.gross_scores_
    {'a': 2, 'b': 0}
    >>> rule.eliminations_[2].rule_.gross_scores_
    {'a': 0}
    >>> rule.winner_
    'a'
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 base_rule: Rule = None, elimination: Elimination = None, propagate_tie_break=True):
        if base_rule is None:
            base_rule = RuleBorda()
        if elimination is None:
            elimination = EliminationLast(k=1)
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter,
            base_rule=base_rule, elimination=elimination, propagate_tie_break=propagate_tie_break
        )
