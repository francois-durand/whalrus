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
from whalrus.rules_committee.rule_committee_scoring import RuleCommitteeScoring
from whalrus.scorers.scorer import Scorer
from whalrus.scorers.scorer_borda import ScorerBorda
from whalrus.priorities.priority import Priority
from whalrus.utils.utils import cached_property, NiceDict, my_division
from numbers import Number
from whalrus.profiles.profile import Profile

class RuleChamberlinCourant(RuleCommitteeScoring):
    # noinspection PyUnresolvedReferences
    """
    A multi-winner rule that select the best committee according to Chamberlin-Courant's voting rule.

    :param scorer: the scorer used to compute the value of the representative candidate for each voter (default:
        :class:`ScorerBorda`).
    :param base_rule_tie_break: a priority rule used to compute the best element of a subset (default:
        :class:`Priority.UNAMBIGUOUS`).

    Each possible committee is assigned a score in the following way: each voter gives the committee a number of points
    equal to her score (in the sense of the scorer) for her most liked candidate in the committee. The committee with
    highest score is elected.

    >>> cc = RuleChamberlinCourant(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    >>> cc.scores_
    {{'a', 'b'}: 8, {'a', 'c'}: 7, {'a', 'd'}: 9, {'b', 'c'}: 6, {'b', 'd'}: 7, {'c', 'd'}: 5}
    >>> cc.winning_committee_
    {'a', 'd'}
    >>> cc.trailing_committee_
    {'c', 'd'}

    >>> cc = RuleChamberlinCourant(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
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

    >>> def gender_balance(committee):
    ...     return abs(sum([candidate[1] == 'Male' for candidate in committee])
    ...                - sum([candidate[1] == 'Female' for candidate in committee])) <= 1
    >>> a, b, c, d = ('a', 'Female'), ('b', 'Male'), ('c', 'Male'), ('d', 'Female')
    >>> cc = RuleChamberlinCourant([[a, b, c, d], [d, b, a, c], [a, b, c, d]], committee_size=2,
    ...                             committee_legality_function=gender_balance)
    >>> cc.winning_committee_
    {('a', 'Female'), ('b', 'Male')}
    """

    def __init__(self, *args, scorer: Scorer = None,
                 base_rule_tie_break: Priority = Priority.UNAMBIGUOUS, **kwargs):
        # Default
        if scorer is None:
            scorer = ScorerBorda()
        self.scorer = scorer
        self.base_rule_tie_break = base_rule_tie_break
        super().__init__(*args, **kwargs)

    def _cc_score(self, committee):

        return sum((
            self.scorer(ballot=ballot, candidates=self.candidates_).scores_[
                ballot.restrict(committee).first(priority=self.base_rule_tie_break)]*weight
            if ballot.restrict(committee).first(priority=self.base_rule_tie_break) is not None
            else 0)
                   for ballot, weight, _ in self.profile_converted_.items())
    
