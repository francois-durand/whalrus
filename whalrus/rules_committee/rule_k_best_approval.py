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
from whalrus.scales.scale_range import ScaleRange
from whalrus.converters_ballot.converter_ballot_to_grades import ConverterBallotToGrades
from whalrus.scorers.scorer_levels import ScorerLevels


class RuleKBestApproval(RuleCommitteeScoring):
    # noinspection PyUnresolvedReferences
    """
    A multi-winner rule that select the best committee according to Best-k Approval voting rule.

    Each possible committee is assigned a score in the following way: each voter gives the committee a number of points
    equal to her score (in the sense of the scorer) for her most liked candidate in the committee. The committee with
    highest score is elected.

    >>> cc = RuleKBestApproval([{'a': 1, 'b': 1, 'c': 0, 'd': 0}, {'d': 1, 'b': 1, 'a': 1, 'c': 0}, {'a': 1, 'b': 0, 'c': 0, 'd': 0}], committee_size=2)
    >>> cc.scores_
    {{'a', 'b'}: 5, {'a', 'c'}: 3, {'a', 'd'}: 4, {'b', 'c'}: 2, {'b', 'd'}: 3, {'c', 'd'}: 1}
    >>> cc.winning_committee_
    {'a', 'b'}
    >>> cc.trailing_committee_
    {'c', 'd'}

    >>> cc = RuleKBestApproval([{'a': 1, 'b': 1, 'c': 0, 'd': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0}],
    ...                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    >>> cc.scores_
    {{'a', 'b'}: 6, {'a', 'c'}: 6, {'a', 'd'}: 4, {'b', 'c'}: 4, {'b', 'd'}: 2, {'c', 'd'}: 2}
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
    >>> cc = RuleKBestApproval([[a, b, c, d], [d, b, a, c], [a, b, c, d]], committee_size=2,
    ...                             committee_legality_function=gender_balance)
    >>> cc.winning_committee_
    {('a', 'Female'), ('b', 'Male')}
    """

    def _cc_score(self, committee):
        converter = ConverterBallotToGrades(scale=ScaleRange(0, 1))
        scorer = ScorerLevels()

        return sum(
            sum(
                scorer(ballot=converter(ballot), candidates=self.candidates_).scores_[candidate]*weight
                for candidate in committee
            )
            for ballot, weight, _ in self.profile_converted_.items()
        )
