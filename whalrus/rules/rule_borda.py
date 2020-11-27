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
from whalrus.rules.rule_score_num_average import RuleScoreNumAverage
from whalrus.scorers.scorer import Scorer
from whalrus.scorers.scorer_borda import ScorerBorda
from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
from whalrus.converters_ballot.converter_ballot import ConverterBallot


class RuleBorda(RuleScoreNumAverage):
    """
    The Borda rule.

    Parameters
    ----------
    args
        Cf. parent class.
    converter : ConverterBallot
        Default: :class:`ConverterBallotToOrder`.
    scorer : Scorer
        Default: :class:`ScorerBorda`.
    kwargs
        Cf. parent class.

    Examples
    --------
        >>> rule = RuleBorda(['a ~ b > c', 'b > c > a'])
        >>> rule.gross_scores_
        {'a': Fraction(3, 2), 'b': Fraction(7, 2), 'c': 1}
        >>> rule.scores_
        {'a': Fraction(3, 4), 'b': Fraction(7, 4), 'c': Fraction(1, 2)}
    """

    def __init__(self, *args, converter: ConverterBallot = None, scorer: Scorer = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToOrder()
        if scorer is None:
            scorer = ScorerBorda()
        super().__init__(*args, converter=converter, scorer=scorer, **kwargs)
