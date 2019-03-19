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
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.converter_ballot.ConverterBallotToLevelsRange import ConverterBallotToLevelsRange
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.scale.ScaleInterval import ScaleInterval
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.scale.ScaleFromSet import ScaleFromSet
from whalrus.scale.ScaleRange import ScaleRange
import logging


class ConverterBallotToLevelsListNonNumeric(ConverterBallot):
    """
    Default converter to a :class:`BallotLevels` using a :class:`ScaleFromList` of levels that are not numbers.

    :param scale: the scale.
    :param borda_unordered_give_points: when converting a :class:`BallotOrder` that is not a :class:`BallotLevels`,
        we use Borda scores as a calculation step. This parameter decides whether the unordered candidates of the
        ballot give points to the ordered candidates. Cf. :class:`ScorerBorda`.

    This converter works essentially the same as :class:`ConverterBallotToLevelsInterval`, but it then maps the
    evaluation to levels of the scale.

    Typical usages:

    >>> converter = ConverterBallotToLevelsListNonNumeric(
    ...     scale=ScaleFromList(['Bad', 'Medium', 'Good', 'Very Good', 'Great', 'Excellent']))
    >>> b = BallotLevels({'a': 1, 'b': .2}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(-1, 1))
    >>> converter(b).as_dict
    {'a': 'Excellent', 'b': 'Very Good'}
    >>> b = BallotLevels({'a': 5, 'b': 4}, candidates={'a', 'b', 'c'}, scale=ScaleRange(0, 5))
    >>> converter(b).as_dict
    {'a': 'Excellent', 'b': 'Great'}
    >>> b = BallotLevels({'a': 4, 'b': 0}, candidates={'a', 'b', 'c'}, scale=ScaleFromSet({-1, 0, 4}))
    >>> converter(b).as_dict
    {'a': 'Excellent', 'b': 'Medium'}
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 'Excellent', 'b': 'Bad', 'c': 'Bad'}
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 'Excellent', 'b': 'Bad', 'c': 'Bad'}
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 'Bad', 'b': 'Excellent', 'c': 'Excellent'}
    >>> converter('a > b > c > d').as_dict
    {'a': 'Excellent', 'b': 'Very Good', 'c': 'Good', 'd': 'Bad'}
    """

    def __init__(self, scale: ScaleFromList, borda_unordered_give_points: bool = True):
        self.scale = scale
        self.borda_unordered_give_points = borda_unordered_give_points

    def __call__(self, x: object, candidates: set =None) -> BallotLevels:
        x = ConverterBallotGeneral()(x, candidates=None)
        if isinstance(x, BallotLevels) and any([level in self.scale.levels for level in x.values()]):
            if all([level in self.scale.levels for level in x.values()]):
                return BallotLevels(x.as_dict, scale=self.scale)
            else:
                logging.warning('Not all levels of ballot ``%s`` are in the scale.' % x)
        x = ConverterBallotToLevelsRange(
            scale=ScaleRange(low=0, high=len(self.scale.levels) - 1),
            borda_unordered_give_points=self.borda_unordered_give_points
        )(x, candidates=None)
        return BallotLevels({c: self.scale.levels[v] for c, v in x.items()},
                            candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
