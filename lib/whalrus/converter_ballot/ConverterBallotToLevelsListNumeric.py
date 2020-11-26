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
from whalrus.converter_ballot.ConverterBallotToLevelsInterval import ConverterBallotToLevelsInterval
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.scale.ScaleInterval import ScaleInterval
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.scale.ScaleFromSet import ScaleFromSet
from whalrus.scale.ScaleRange import ScaleRange
from whalrus.utils.Utils import take_closest


class ConverterBallotToLevelsListNumeric(ConverterBallot):
    """
    Default converter to a :class:`BallotLevels` using a :class:`ScaleFromList` of numbers.

    :param scale: the scale.
    :param borda_unordered_give_points: when converting a :class:`BallotOrder` that is not a :class:`BallotLevels`,
        we use Borda scores as a calculation step. This parameter decides whether the unordered candidates of the
        ballot give points to the ordered candidates. Cf. :class:`ScorerBorda`.

    This converter works essentially the same as :class:`ConverterBallotToLevelsInterval`, but it then maps the
    evaluations to levels of the scale.

    Typical usages:

    >>> converter = ConverterBallotToLevelsListNumeric(scale=ScaleFromList([-1, 0, 3, 4]))
    >>> b = BallotLevels({'a': 1, 'b': .2}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(-1, 1))
    >>> converter(b).as_dict
    {'a': 4, 'b': 3}
    >>> b = BallotLevels({'a': 5, 'b': 4}, candidates={'a', 'b', 'c'}, scale=ScaleRange(0, 5))
    >>> converter(b).as_dict
    {'a': 4, 'b': 3}
    >>> b = BallotLevels({'a': 4, 'b': 0}, candidates={'a', 'b', 'c'}, scale=ScaleFromSet({-1, 0, 4}))
    >>> converter(b).as_dict
    {'a': 4, 'b': 0}
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 4, 'b': -1, 'c': -1}
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 4, 'b': -1, 'c': -1}
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': -1, 'b': 4, 'c': 4}
    >>> converter('a > b > c > d').as_dict
    {'a': 4, 'b': 3, 'c': 0, 'd': -1}
    """

    def __init__(self, scale: ScaleFromList, borda_unordered_give_points: bool=True):
        self.scale = scale
        self.borda_unordered_give_points = borda_unordered_give_points

    def __call__(self, x: object, candidates: set =None) -> BallotLevels:
        if not self.scale.is_numeric:
            raise ValueError('The scale should be numeric.')
        # noinspection PyTypeChecker
        x = ConverterBallotToLevelsInterval(
            scale=ScaleInterval(low=self.scale.low, high=self.scale.high),
            borda_unordered_give_points=self.borda_unordered_give_points
        )(x, candidates=None)
        return BallotLevels({c: take_closest(self.scale.levels, v) for c, v in x.items()},
                            candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
