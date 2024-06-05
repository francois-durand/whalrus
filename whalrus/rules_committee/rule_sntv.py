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
from whalrus.rules_committee.rule_committee_average import RuleCommitteeAverage
from whalrus.rules_committee.rule_committee_scoring import RuleCommitteeScoring
from whalrus.converters_ballot.converter_ballot_to_plurality import ConverterBallotToPlurality
from whalrus.scorers.scorer_plurality import ScorerPlurality
from whalrus.priorities.priority_lifted_leximax import PriorityLiftedLeximax
from whalrus.priorities.priority import Priority

class RuleSNTV(RuleCommitteeAverage):
    # noinspection PyUnresolvedReferences
    """
    A multi-winner rule that select the best committee according to Bloc voting rule.

    Each possible committee is assigned a score using k-approval scoring function. The committee with
    highest score is elected.

    >>> cc = RuleSNTV(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    >>> cc.gross_scores
    {{'a', 'b'}: 2, {'a', 'c'}: 2, {'a', 'd'}: 3, {'b', 'c'}: 0, {'b', 'd'}: 1, {'c', 'd'}: 1}
    >>> cc.winning_committee_
    {'a', 'd'}
    >>> cc.trailing_committee_
    {'b', 'c'}

    >>> cc = RuleSNTV(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
    ...                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    >>> cc.gross_scores
    {{'a', 'b'}: 4, {'a', 'c'}: 4, {'a', 'd'}: 4, {'b', 'c'}: 0, {'b', 'd'}: 0, {'c', 'd'}: 0}
    >>> cc.cowinning_committees_
    {{'a', 'b'}, {'a', 'c'}, {'a', 'd'}}
    >>> cc.winning_committee_
    {'a', 'b'}
    >>> cc.cotrailing_committees_
    {{'b', 'c'}, {'b', 'd'}, {'c', 'd'}}
    >>> cc.trailing_committee_
    {'c', 'd'}

    >>> def gender_balance(committee):
    ...     return abs(sum([candidate[1] == 'Male' for candidate in committee])
    ...                - sum([candidate[1] == 'Female' for candidate in committee])) <= 1
    >>> a, b, c, d = ('a', 'Female'), ('b', 'Male'), ('c', 'Male'), ('d', 'Female')
    >>> cc = RuleSNTV([[a, b, c, d], [d, b, a, c], [a, b, c, d]], committee_size=2,
    ...                             committee_legality_function=gender_balance)
    >>> cc.cowinning_committees_
    {{('a', 'Female'), ('b', 'Male')}, {('a', 'Female'), ('c', 'Male')}}
   """

    def __init__(self, *args, committee_size : int,  **kwargs):
        
        
        super().__init__(*args,committee_size = committee_size, **kwargs)
        self.converter = ConverterBallotToPlurality()
        self.scorer = ScorerPlurality()
    
if __name__ == '__main__':
    cc = RuleSNTV(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)

    print(cc.winning_committee_)