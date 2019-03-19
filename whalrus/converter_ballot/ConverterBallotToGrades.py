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
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.scale.Scale import Scale
from whalrus.scale.ScaleInterval import ScaleInterval
from whalrus.scale.ScaleRange import ScaleRange
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.scale.ScaleFromSet import ScaleFromSet
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotToLevelsInterval import ConverterBallotToLevelsInterval
from whalrus.converter_ballot.ConverterBallotToLevelsRange import ConverterBallotToLevelsRange
from whalrus.converter_ballot.ConverterBallotToLevelsListNumeric import ConverterBallotToLevelsListNumeric


class ConverterBallotToGrades(ConverterBallot):
    """
    Default converter to a :class:`BallotLevels` using numeric grades.

    :param scale: a numeric :class:`Scale`. If specified, then the ballot will be converted to this scale. If it is
        None, then any ballot that is of class :class:`BallotLevels` and numeric will be kept as it is, and any other
        ballot will converted to a :class:`BallotLevels` using a :class:`ScaleInterval` with bounds 0 and 1
    :param borda_unordered_give_points: when converting a :class:`BallotOrder` that is not a :class:`BallotLevels`,
        we use Borda scores as a calculation step. This parameter decides whether the unordered candidates of the
        ballot give points to the ordered candidates. Cf. :class:`ScorerBorda`.

    This is a default converter to a :class:`BallotLevels` using numeric grades. It tries to infer the type of input
    and converts it to a :class:`BallotLevels`, with a numeric scale. It is a wrapper for the specialized converters
    :class:`ConverterBallotToLevelsInterval`, :class:`ConverterBallotToLevelsRange`,
    and :class:`ConverterBallotToLevelsListNumeric`.

    Typical usages:

    >>> ballot = BallotLevels({'a': 100, 'b': 57}, scale=ScaleRange(0, 100))
    >>> ConverterBallotToGrades(scale=ScaleInterval(low=0, high=10))(ballot).as_dict
    {'a': 10, 'b': Fraction(57, 10)}
    >>> ConverterBallotToGrades(scale=ScaleRange(low=0, high=10))(ballot).as_dict
    {'a': 10, 'b': 6}
    >>> ConverterBallotToGrades(scale=ScaleFromSet({0, 2, 4, 10}))(ballot).as_dict
    {'a': 10, 'b': 4}

    >>> ballot = BallotLevels({'a': 'Good', 'b': 'Medium'},
    ...                       scale=ScaleFromList(['Bad', 'Medium', 'Good']))
    >>> ConverterBallotToGrades()(ballot).as_dict
    {'a': 1, 'b': Fraction(1, 2)}

    For more examples, cf. :class:`ConverterBallotToLevelsInterval`, :class:`ConverterBallotToLevelsRange`,
    and :class:`ConverterBallotToLevelsListNumeric`.
    """

    def __init__(self, scale: Scale = None, borda_unordered_give_points: bool = True):
        self.scale = scale
        self.borda_unordered_give_points = borda_unordered_give_points
        if scale is None:
            self._aux_converter = ConverterBallotToLevelsInterval(
                scale=ScaleInterval(low=0, high=1), borda_unordered_give_points=borda_unordered_give_points)
        elif isinstance(scale, ScaleInterval):
            self._aux_converter = ConverterBallotToLevelsInterval(
                scale=scale, borda_unordered_give_points=borda_unordered_give_points)
        elif isinstance(scale, ScaleRange):
            self._aux_converter = ConverterBallotToLevelsRange(
                scale=scale, borda_unordered_give_points=borda_unordered_give_points)
        elif isinstance(scale, ScaleFromList):
            self._aux_converter = ConverterBallotToLevelsListNumeric(
                scale=scale, borda_unordered_give_points=borda_unordered_give_points)
        else:
            raise NotImplementedError

    def __call__(self, x: object, candidates: set =None) -> BallotLevels:
        if self.scale is None and isinstance(x, BallotLevels) and x.is_numeric:
            return x.restrict(candidates=candidates)
        return self._aux_converter(x, candidates=candidates)
