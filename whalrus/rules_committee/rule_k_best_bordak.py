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
from whalrus.converters_ballot.converter_ballot_to_strict_order import ConverterBallotToStrictOrder
from whalrus.scorers.scorer_borda import ScorerBorda
from whalrus.rules.rule import Rule
from whalrus.rules.rule_borda import RuleBorda
from whalrus.rules_committee.rule_k_best import RuleKBest
from whalrus.priorities.priority_lifted_leximax import PriorityLiftedLeximax
from whalrus.priorities.priority import Priority

class RuleKBestBordak(RuleKBest):
    # noinspection PyUnresolvedReferences
    """
    A multi-winner rule that select the best committee according to Best-k Borda voting rule.

    Each possible committee is assigned a score in the following way: each voter gives the committee a number of points
    equal to her score (in the sense of the scorer) for her most liked candidate in the committee. The committee with
    highest score is elected.

    >>> cc = RuleKBestBordak(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)

    >>> cc.winning_committee_
    {'a', 'b'}
    >>> cc.trailing_committee_
    {'c', 'd'}

    >>> cc = RuleKBestBordak(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
    ...                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING),use_base_rule_tie_break = False)

    >>> cc.cowinning_committees_
    {{'a', 'b'}, {'a', 'c'}}
    >>> cc.winning_committee_
    {'a', 'b'}
    >>> cc.cotrailing_committees_
    {{'b', 'd'}, {'c', 'd'}}
    >>> cc.trailing_committee_
    {'c', 'd'}

    """

    def __init__(self, *args, committee_size : int, base_rule : Rule = None, scorer = None,  **kwargs):
        
        self.converter = ConverterBallotToStrictOrder()
        
        if scorer is None:
            scorer = ScorerBorda()
        self.scorer = scorer
        if base_rule is None:
            base_rule = RuleBorda(scorer=self.scorer, converter = self.converter, tie_break=Priority.ASCENDING)
        super().__init__(*args,base_rule = base_rule,committee_size = committee_size, **kwargs)
