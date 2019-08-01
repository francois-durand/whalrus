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
from whalrus.scorer.Scorer import Scorer
from whalrus.scorer.ScorerBorda import ScorerBorda
from whalrus.rule.multiwinner.RuleMultiWinner import RuleMultiWinner
from whalrus.utils.Utils import cached_property, NiceSet, NiceFrozenSet, NicePowerSet
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.priority.Priority import Priority
from whalrus.priority.SetPriority import LiftedSetPriority
from whalrus.profile.Profile import Profile
from itertools import combinations
from typing import Union


class RuleMultiWinnerCC(RuleMultiWinner):
    """
    A multiwinner rule that select the best committee according to
    Chamberlin-Courant's voting rule.

    :param scorer: the scoring vector used to compute the value of
    the representative for each voter (default: Borda).

    >>> cc = RuleMultiWinnerCC(['a > b > c > d', 'd > b > a > c',
    ...     'a > b > c > d'], committee_size=2)
    >>> cc.cowinners_
    {{'a', 'd'}}
    >>> cc.cotrailers_
    {{'c', 'd'}}

    >>> cc = RuleMultiWinnerCC(['a > b > c > d', 'a > c > b > d',
    ...     'a > c > b > d', 'a > b > c > d'], committee_size=2)
    >>> cc.cowinners_
    {{'a', 'b'}, {'a', 'c'}, {'a', 'd'}}
    >>> print(cc.cotrailers_)
    {{'b', 'd'}, {'c', 'd'}}
    >>> try:
    ...     cc.winner_
    ... except ValueError:
    ...     print('Cannot choose winner')
    Cannot choose winner
    >>> cc.tie_break = LiftedSetPriority.LEXIMAX
    >>> cc.tie_break.base_priority = Priority.ASCENDING
    >>> print(cc.winner_)
    {'a', 'b'}
    >>> print(cc.trailer_)
    {'c', 'd'}


    """

    def __init__(self, ballots: Union[list, Profile] = None,
                 weights: list = None, voters: list = None,
                 candidates: set = None, committee_size: int = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS,
                 converter: ConverterBallot = None,
                 scorer: Scorer = None):
        self.scorer = scorer
        if scorer is None:
            self.scorer = ScorerBorda
        super().__init__(
            ballots=ballots, weights=weights, voters=voters,
            candidates=candidates,
            committee_size=committee_size,
            tie_break=tie_break, converter=converter
        )

    def _all_committees(self):
        yield from (
            NiceFrozenSet(c)
            for c in combinations(self.candidates_, self.committee_size))

    def _cc_score(self, committee):
        return sum(self
                   .scorer(ballot=ballot, candidates=self.candidates_)
                   .scores_[ballot.restrict(committee).first()]
                   for ballot in self.profile_converted_)

    @cached_property
    def cowinners_(self) -> NiceSet:
        if self.committee_size is None:
            raise ValueError("The committee size is not set.")
        base_set = set()
        current_max = 0
        for committee in self._all_committees():
            current_score = self._cc_score(committee)
            if current_score == current_max:
                base_set.add(committee)
            if current_score > current_max:
                base_set = {committee}
                current_max = current_score
        return NicePowerSet(NiceFrozenSet(base_set))

    @cached_property
    def cotrailers_(self) -> NiceSet:
        if self.committee_size is None:
            raise ValueError("The committee size is not set.")
        base_set = set()
        current_min = self.committee_size * max(
            self
            .scorer(ballot=ballot, candidates=self.candidates_)
            .scores_[ballot.first()]
            for ballot in self.profile_converted_)
        for committee in self._all_committees():
            current_score = self._cc_score(committee)
            if current_score == current_min:
                base_set.add(committee)
            if current_score < current_min:
                base_set = {committee}
                current_min = current_score
        return NicePowerSet(NiceFrozenSet(base_set))

    @cached_property
    def winner_(self) -> object:
        return self.tie_break.choice(self.cowinners_)

    @cached_property
    def trailer_(self) -> object:
        return self.tie_break.choice(self.cotrailers_, reverse=True)
