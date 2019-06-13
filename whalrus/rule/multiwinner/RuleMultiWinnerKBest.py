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
from whalrus.rule.Rule import Rule
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.rule.multiwinner.RuleMultiWinner import RuleMultiWinner
from whalrus.utils.Utils import cached_property, NiceSet, NiceFrozenSet, NicePowerSet
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.priority.Priority import Priority
from whalrus.priority.SetPriority import LiftedSetPriority
from whalrus.profile.Profile import Profile
from itertools import combinations
from typing import Union


class RuleMultiWinnerKBest(RuleMultiWinner):
    """
    A multiwinner rule that select the best k candidates of a single winner
    voting rule.

    :param rule: a single winner voting rule that will be used to rank
    the candidates.

    >>> kbest = RuleMultiWinnerKBest(['a > b > c > d', 'd > b > a > c',
    ...           'a > b > c > d'], committee_size=2)
    >>> kbest.cowinners_
    {{'a', 'b'}}
    >>> kbest.cotrailers_
    {{'c', 'd'}}

    >>> kbest = RuleMultiWinnerKBest(['a > b > c > d', 'a > c > b > d',
    ...           'a > c > b > d', 'a > b > c > d'], committee_size=2)
    >>> kbest.cowinners_
    {{'a', 'b'}, {'a', 'c'}}
    >>> print(kbest.cotrailers_)
    {{'b', 'd'}, {'c', 'd'}}
    >>> try:
    ...     kbest.winner_
    ... except ValueError:
    ...     print('Cannot choose winner')
    Cannot choose winner
    >>> kbest.tie_break = LiftedSetPriority.LEXIMAX
    >>> kbest.tie_break.base_priority = Priority.ASCENDING
    >>> print(kbest.winner_)
    {'a', 'b'}
    >>> print(kbest.trailer_)
    {'c', 'd'}


    """

    def __init__(self, ballots: Union[list, Profile] = None,
                 weights: list = None, voters: list = None,
                 candidates: set = None, committee_size: int = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS,
                 converter: ConverterBallot = None,
                 base_rule: Rule = None):
        self.base_rule = base_rule
        if base_rule is None:
            self.base_rule = RuleBorda
        super().__init__(
            ballots=ballots, weights=weights, voters=voters,
            candidates=candidates,
            committee_size=committee_size,
            tie_break=tie_break, converter=converter
        )

    @cached_property
    def cowinners_(self) -> NiceSet:
        if self.committee_size is None:
            raise ValueError("The committee size is not set.")
        base_set = set()
        candidates = self.candidates_
        rule = self.base_rule
        rule = rule(ballots=self.profile_converted_, candidates=candidates)
        for equivalence_class in rule.order_:
            missing_candidates = self.committee_size - len(base_set)
            if len(equivalence_class) >= missing_candidates:
                committees = NicePowerSet(
                    NiceFrozenSet(base_set.union(subset))
                    for subset in combinations(equivalence_class,
                                               missing_candidates)
                )
                return committees
            base_set.update(equivalence_class)

    @cached_property
    def cotrailers_(self) -> NiceSet:
        if self.committee_size is None:
            raise ValueError("The committee size is not set.")
        base_set = set()
        candidates = self.candidates_
        rule = self.base_rule
        rule = rule(ballots=self.profile_converted_, candidates=candidates)
        for equivalence_class in reversed(rule.order_):
            missing_candidates = self.committee_size - len(base_set)
            if len(equivalence_class) >= missing_candidates:
                committees = NicePowerSet(
                    NiceFrozenSet(base_set.union(subset))
                    for subset in combinations(equivalence_class,
                                               missing_candidates)
                )
                return committees
            base_set.update(equivalence_class)

    @cached_property
    def winner_(self) -> object:
        return self.tie_break.choice(self.cowinners_)

    @cached_property
    def trailer_(self) -> object:
        return self.tie_break.choice(self.cotrailers_, reverse=True)
