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
from whalrus.converters_ballot.converter_ballot_to_strict_order import ConverterBallotToStrictOrder
from whalrus.scorers.scorer_borda import ScorerBorda


class RuleKBestBorda(RuleCommitteeScoring):
    # noinspection PyUnresolvedReferences
    """
    A multi-winner rule that select the best committee according to Best-k Borda voting rule.

    Each possible committee is assigned a score in the following way: each voter gives the committee a number of points
    equal to her score (in the sense of the scorer) for her most liked candidate in the committee. The committee with
    highest score is elected.

    >>> cc = RuleKBestBorda(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    >>> cc.scores_
    {{'a', 'b'}: 13, {'a', 'c'}: 9, {'a', 'd'}: 10, {'b', 'c'}: 8, {'b', 'd'}: 9, {'c', 'd'}: 5}
    >>> cc.winning_committee_
    {'a', 'b'}
    >>> cc.trailing_committee_
    {'c', 'd'}

    >>> cc = RuleKBestBorda(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
    ...                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    >>> cc.scores_
    {{'a', 'b'}: 18, {'a', 'c'}: 18, {'a', 'd'}: 12, {'b', 'c'}: 12, {'b', 'd'}: 6, {'c', 'd'}: 6}
    >>> cc.cowinning_committees_
    {{'a', 'b'}, {'a', 'c'}}
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
    >>> cc = RuleKBestBorda([[a, b, c, d], [d, b, a, c], [a, b, c, d]], committee_size=2,
    ...                             committee_legality_function=gender_balance)
    >>> cc.winning_committee_
    {('a', 'Female'), ('b', 'Male')}
    """

    def _cc_score(self, committee):
        converter = ConverterBallotToStrictOrder()
        scorer = ScorerBorda()

        return sum(
            sum(
                scorer(ballot=converter(ballot), candidates=self.candidates_).scores_[candidate]*weight
                for candidate in committee
            )
            for ballot, weight, _ in self.profile_converted_.items()
        )
