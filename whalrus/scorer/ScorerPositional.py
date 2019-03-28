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
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.utils.Utils import cached_property, NiceDict, convert_number
from whalrus.scorer.Scorer import Scorer
from numbers import Number
from typing import Union


class ScorerPositional(Scorer):
    """
    A positional scorer for strict order ballots.

    :param `*args`: cf. parent class.
    :param points_scheme: the list of points to be attributed to the (first) candidates of a ballot.
    :param points_fill: points for ordered candidates that have a rank beyond the ``points_scheme``.
    :param points_unordered: points for the unordered candidates.
    :param points_absent: points for the absent candidates.
    :param `**kwargs`: cf. parent class.

    The top candidate in the ballot receives ``points_scheme[0]`` points, the second one receives ``points_scheme[1]``
    points, etc:

    >>> ScorerPositional(ballot=BallotOrder('a > b > c'), points_scheme=[10, 5, 3]).scores_
    {'a': 10, 'b': 5, 'c': 3}

    The points scheme does not need to have the same length as the ballot:

    >>> ScorerPositional(ballot=BallotOrder('a > b > c'), points_scheme=[3, 2, 1, .5]).scores_
    {'a': 3, 'b': 2, 'c': 1}
    >>> ScorerPositional(ballot=BallotOrder('a > b > c'), points_scheme=[3, 2]).scores_
    {'a': 3, 'b': 2, 'c': 0}

    A typical usage of this is k-Approval voting:

    >>> ScorerPositional(ballot=BallotOrder('a > b > c > d > e'), points_scheme=[1, 1]).scores_
    {'a': 1, 'b': 1, 'c': 0, 'd': 0, 'e': 0}

    In the example below, candidates `a`, `b` and `c` are "ordered", `d` is "unordered", and `e` is "absent"
    in the ballot, meaning that `e` was not even available when the voter cast her ballot. The options of the
    scorer provide different ways to take these special cases into account:

    >>> ballot=BallotOrder('a > b > c', candidates={'a', 'b', 'c', 'd'})
    >>> candidates_election = {'a', 'b', 'c', 'd', 'e'}
    >>> ScorerPositional(ballot, candidates=candidates_election, points_scheme=[3, 2]).scores_
    {'a': 3, 'b': 2, 'c': 0, 'd': 0}
    >>> ScorerPositional(ballot, candidates=candidates_election, points_scheme=[3, 2],
    ...     points_fill=-1, points_unordered=-2, points_absent=-3).scores_
    {'a': 3, 'b': 2, 'c': -1, 'd': -2, 'e': -3}
    >>> ScorerPositional(ballot, candidates=candidates_election, points_scheme=[3, 2],
    ...     points_fill=None, points_unordered=None, points_absent=None).scores_
    {'a': 3, 'b': 2}
    """

    def __init__(self, *args,
                 points_scheme: list = None, points_fill: Union[Number, None] = 0,
                 points_unordered: Union[Number, None] = 0, points_absent: Union[Number, None] = None, **kwargs):
        self.points_scheme = [convert_number(x) for x in points_scheme]
        self.points_fill = convert_number(points_fill)
        self.points_unordered = convert_number(points_unordered)
        self.points_absent = convert_number(points_absent)
        super().__init__(*args, **kwargs)

    @cached_property
    def scores_(self) -> NiceDict:
        scores = NiceDict()
        l_points_scheme = len(self.points_scheme)
        for i, c in enumerate(self.ballot_):
            if i < l_points_scheme:
                scores[c] = self.points_scheme[i]
            else:
                if self.points_fill is None:
                    break
                scores[c] = self.points_fill
        if self.points_unordered is not None:
            scores.update({c: self.points_unordered for c in self.ballot_.candidates_not_in_b})
        if self.points_absent is not None:
            scores.update({c: self.points_absent for c in self.candidates_ - self.ballot_.candidates})
        return scores
