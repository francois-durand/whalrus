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
from whalrus.scorer.ScorerPositional import ScorerPositional
from whalrus.converter_ballot.ConverterBallotToStrictOrder import ConverterBallotToStrictOrder
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallot import ConverterBallot


class RuleScorePositional(RuleScoreNumAverage):
    """
    A positional scoring rule.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToStrictOrder`.
    :param points_scheme: the list of points to be attributed to the candidates of a ballot.
        Cf. :class:`ScorerPositional`.
    :param `**kwargs`: cf. parent class.

    >>> RuleScorePositional(['a > b > c', 'b > c > a'], points_scheme=[3, 2, 1]).gross_scores_
    {'a': 4, 'b': 5, 'c': 3}

    Since this voting rule needs strict orders, problems may occur as soon as there is indifference in the ballots. To
    avoid these issues, specify the ballot converter explicitly:

    >>> RuleScorePositional(['a > b ~ c', 'b > c > a'], points_scheme=[1, 1, 0],
    ...     converter=ConverterBallotToStrictOrder(priority=Priority.ASCENDING)).gross_scores_
    {'a': 1, 'b': 2, 'c': 1}
    """

    def __init__(self, *args, converter: ConverterBallot = None, points_scheme: list = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToStrictOrder()
        super().__init__(*args, converter=converter, scorer=ScorerPositional(points_scheme=points_scheme),
                         default_average=0, **kwargs)
