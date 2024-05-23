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
from whalrus.scorers.scorer_positional import ScorerPositional
from whalrus.utils.utils import cached_property, NiceDict, my_division
from numbers import Number


class RuleBloc(RuleCommitteeScoring):
    # noinspection PyUnresolvedReferences
    """
    A multi-winner rule that select the best committee according to Bloc voting rule.

    Each possible committee is assigned a score using k-approval scoring function. The committee with
    highest score is elected.

    >>> cc = RuleBloc(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    >>> cc.scores_
    {{'a', 'b'}: 5, {'a', 'c'}: 2, {'a', 'd'}: 3, {'b', 'c'}: 3, {'b', 'd'}: 4, {'c', 'd'}: 1}
    >>> cc.winning_committee_
    {'a', 'b'}
    >>> cc.trailing_committee_
    {'c', 'd'}

    >>> cc = RuleBloc(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
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
    >>> cc = RuleBloc([[a, b, c, d], [d, b, a, c], [a, b, c, d]], committee_size=2,
    ...                             committee_legality_function=gender_balance)
    >>> cc.winning_committee_
    {('a', 'Female'), ('b', 'Male')}
    """
    @cached_property
    def _gross_scores_and_weights_(self) -> dict:
        gross_scores = NiceDict({c: 0 for c in self.candidates_})
        weights = NiceDict({c: 0 for c in self.candidates_})
        for ballot, weight, voter in self.profile_converted_.items():
            for c, value in self.scorer(ballot=ballot, voter=voter, candidates=self.candidates_).scores_.items():
                gross_scores[c] += weight * value
                weights[c] += weight
        return {'gross_scores': gross_scores, 'weights': weights}

    @cached_property
    def weights_(self) -> NiceDict:
        """NiceDict: The weights used for the candidates. For each candidate, this dictionary gives the total weight
        for this candidate, i.e. the total weight of all voters who assign a score to this candidate. This is the
        denominator in the candidate's average score.
        """
        return self._gross_scores_and_weights_['weights']
    
    @cached_property
    def gross_scores_(self) -> NiceDict:
        """NiceDict: The gross scores of the candidates. For each candidate, this dictionary gives the sum of its
        scores, multiplied by the weights of the corresponding voters. This is the numerator in the candidate's average
        score.
        """
        return self._gross_scores_and_weights_['gross_scores']


    @cached_property
    def scores(self) -> NiceDict:
        self.default_average = 0
        return NiceDict({c: my_division(score, self.weights_[c], divide_by_zero=self.default_average)
                         for c, score in self.gross_scores_.items()})

    def _cc_score(self, committee):
        converter = ConverterBallotToStrictOrder()
        self.scorer = ScorerPositional(points_scheme=[1] * len(committee))

        score = self.scores
        return sum(
                score[candidate] for candidate in committee
        )