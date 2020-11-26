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
from whalrus.scale.ScaleRange import ScaleRange
from whalrus.scorer.Scorer import Scorer
from whalrus.scorer.ScorerLevels import ScorerLevels
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.rule.RuleScoreNumAverage import RuleScoreNumAverage
from whalrus.converter_ballot.ConverterBallotToGrades import ConverterBallotToGrades
from whalrus.converter_ballot.ConverterBallot import ConverterBallot


class RuleRangeVoting(RuleScoreNumAverage):
    """
    Range voting.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToGrades`.
    :param scorer: the default is :class:`ScorerLevels`.
    :param `**kwargs`: cf. parent class.

    Typical usage:

    >>> RuleRangeVoting([{'a': 1, 'b': .8, 'c': .2}, {'a': 0, 'b': .6, 'c': 1}]).scores_
    {'a': Fraction(1, 2), 'b': Fraction(7, 10), 'c': Fraction(3, 5)}
    >>> RuleRangeVoting([{'a': 10, 'b': 8, 'c': 2}, {'a': 0, 'b': 6, 'c': 10}]).scores_
    {'a': 5, 'b': 7, 'c': 6}

    The following examples use the ballot converter:

    >>> RuleRangeVoting(['a > b > c']).profile_converted_[0].as_dict
    {'a': 1, 'b': Fraction(1, 2), 'c': 0}
    >>> RuleRangeVoting(
    ...     ['a > b > c'], converter=ConverterBallotToGrades(scale=ScaleRange(0, 10))
    ... ).profile_converted_[0].as_dict
    {'a': 10, 'b': 5, 'c': 0}

    To examine the effect of the options, let us examine:

    >>> b1 = BallotLevels({'a': 8, 'b': 10}, candidates={'a', 'b'})
    >>> b2 = BallotLevels({'a': 6, 'c': 10}, candidates={'a', 'b', 'c'})

    In ballot ``b1``, candidate `c` is absent, which means that the candidate was not even available when the voter
    cast her ballot. In ballot ``b2``, candidate `b` is ungraded: it was available, but the voter decided not to give
    it a grade. By the way, we will also introduce a candidate `d` who receives no evaluation at all. Here are several
    possible settings for the voting rule, along with their consequences:

    >>> RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'}).scores_
    {'a': 7, 'b': 10, 'c': 10, 'd': 0}
    >>> RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'}, default_average=5).scores_
    {'a': 7, 'b': 10, 'c': 10, 'd': 5}
    >>> RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'},
    ...     scorer=ScorerLevels(level_ungraded=0)).scores_
    {'a': 7, 'b': 5, 'c': 10, 'd': 0}
    >>> RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'},
    ...     scorer=ScorerLevels(level_ungraded=0, level_absent=0)).scores_
    {'a': 7, 'b': 5, 'c': 5, 'd': 0}

    For more information, cf. :class:`ScorerLevels`.
    """

    def __init__(self, *args, converter: ConverterBallot = None, scorer: Scorer = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToGrades()
        if scorer is None:
            scorer = ScorerLevels()
        super().__init__(*args, converter=converter, scorer=scorer, **kwargs)
