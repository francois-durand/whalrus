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
from whalrus.rule.RuleScoreNumAverage import RuleScoreNumAverage
from whalrus.scorer.Scorer import Scorer
from whalrus.scorer.ScorerBorda import ScorerBorda
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.profile.Profile import Profile
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union
from numbers import Number


class RuleBorda(RuleScoreNumAverage):
    """
    The Borda rule.

    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param scorer: the default is :class:`ScorerBorda`.

    >>> rule = RuleBorda(['a ~ b > c', 'b > c > a'])
    >>> rule.gross_scores_
    {'a': Fraction(3, 2), 'b': Fraction(7, 2), 'c': 1}
    >>> rule.scores_
    {'a': Fraction(3, 4), 'b': Fraction(7, 4), 'c': Fraction(1, 2)}
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 scorer: Scorer = None, default_average: Number = None):
        if converter is None:
            converter = ConverterBallotToOrder()
        if scorer is None:
            scorer = ScorerBorda()
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter,
            scorer=scorer, default_average=default_average
        )
