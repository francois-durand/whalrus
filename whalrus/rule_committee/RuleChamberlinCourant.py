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
from whalrus.utils.Utils import cached_property, NiceSet, NiceFrozenSet, NiceDict
from whalrus.priority.Priority import Priority
from whalrus.priority.PriorityLiftedLeximax import PriorityLiftedLeximax
from whalrus.rule_committee.RuleCommittee import RuleCommittee
from whalrus.scorer.Scorer import Scorer
from whalrus.scorer.ScorerBorda import ScorerBorda
from itertools import combinations


class RuleChamberlainCourant(RuleCommittee):
    """
    A multi-winner rule that select the best committee according to Chamberlin-Courant's voting rule.

    :param committee_size: the number of candidates that will be elected in the committee.
    :param scorer: the scorer used to compute the value of the representative candidate for each voter (default:
        :class:`ScorerBorda`).

    Each possible committee is assigned a score in the following way: each voter gives the committee a number of points
    equal to her score (in the sense of the scorer) for her most liked candidate in the committee. The committee with
    highest score is elected.

    >>> cc = RuleChamberlainCourant(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    >>> cc.scores_
    {{'a', 'b'}: 8, {'a', 'c'}: 7, {'a', 'd'}: 9, {'b', 'c'}: 6, {'b', 'd'}: 7, {'c', 'd'}: 5}
    >>> cc.winning_committee_
    {'a', 'd'}
    >>> cc.trailing_committee_
    {'c', 'd'}

    >>> cc = RuleChamberlainCourant(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
    ...                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    >>> cc.scores_
    {{'a', 'b'}: 12, {'a', 'c'}: 12, {'a', 'd'}: 12, {'b', 'c'}: 8, {'b', 'd'}: 6, {'c', 'd'}: 6}
    >>> cc.cowinning_committees_
    {{'a', 'b'}, {'a', 'c'}, {'a', 'd'}}
    >>> cc.winning_committee_
    {'a', 'b'}
    >>> cc.cotrailing_committees_
    {{'b', 'd'}, {'c', 'd'}}
    >>> cc.trailing_committee_
    {'c', 'd'}
    """

    def __init__(self, *args, committee_size: int, scorer: Scorer = None, **kwargs):
        # Default
        if scorer is None:
            scorer = ScorerBorda()
        # Parameters
        self.committee_size = committee_size
        self.scorer = scorer
        super().__init__(*args, **kwargs)

    def _all_committees(self):
        yield from (NiceFrozenSet(s) for s in combinations(self.candidates_, self.committee_size))

    def _cc_score(self, committee):
        return sum(self.scorer(ballot=ballot, candidates=self.candidates_).scores_[ballot.restrict(committee).first()]
                   for ballot in self.profile_converted_)

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
