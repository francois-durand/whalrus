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
import numbers
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.scale.Scale import Scale
from whalrus.scale.ScaleInterval import ScaleInterval
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.scale.ScaleFromSet import ScaleFromSet
from whalrus.scale.ScaleRange import ScaleRange
from whalrus.scorer.ScorerBorda import ScorerBorda
from whalrus.utils.Utils import my_division


class ConverterBallotToLevelsInterval(ConverterBallot):
    """
    Default converter to a :class:`BallotLevels` using a :class:`ScaleInterval` (interval of real numbers).

    :param scale: a :class:`ScaleInterval`.
    :param borda_unordered_give_points: when converting a :class:`BallotOrder` that is not a :class:`BallotLevels`, we
        use Borda scores (normalized to the interval [``scale.low``, ``scale.high``]. This parameter decides whether
        the unordered candidates of the ballot give points to the ordered candidates. Cf. :class:`ScorerBorda`.

    Typical usages:

    >>> converter = ConverterBallotToLevelsInterval()
    >>> b = BallotLevels({'a': 1, 'b': .5}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(-1, 1))
    >>> converter(b).as_dict
    {'a': 1, 'b': Fraction(3, 4)}
    >>> b = BallotLevels({'a': 5, 'b': 4}, candidates={'a', 'b', 'c'}, scale=ScaleRange(0, 5))
    >>> converter(b).as_dict
    {'a': 1, 'b': Fraction(4, 5)}
    >>> b = BallotLevels({'a': 3, 'b': 0}, candidates={'a', 'b', 'c'}, scale=ScaleFromSet({-1, 0, 3}))
    >>> converter(b).as_dict
    {'a': 1, 'b': Fraction(1, 4)}
    >>> b = BallotLevels({'a': 'Excellent', 'b': 'Very Good'}, candidates={'a', 'b', 'c'},
    ...                  scale=ScaleFromList(['Bad', 'Medium', 'Good', 'Very Good', 'Excellent']))
    >>> converter(b).as_dict
    {'a': 1, 'b': Fraction(3, 4)}
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 1, 'b': 0, 'c': 0}
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 1, 'b': 0, 'c': 0}
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'})).as_dict
    {'a': 0, 'b': 1, 'c': 1}
    >>> converter('a > b > c').as_dict
    {'a': 1, 'b': Fraction(1, 2), 'c': 0}

    Options for converting ordered ballots:

    >>> b = BallotOrder('a > b > c', candidates={'a', 'b', 'c', 'd', 'e'})
    >>> ConverterBallotToLevelsInterval(borda_unordered_give_points=False)(b).as_dict
    {'a': 1, 'b': Fraction(1, 2), 'c': 0}
    >>> ConverterBallotToLevelsInterval(borda_unordered_give_points=True)(b).as_dict
    {'a': 1, 'b': Fraction(3, 4), 'c': Fraction(1, 2)}
    """

    def __init__(self, scale: Scale = ScaleInterval(0, 1), borda_unordered_give_points: bool = True):
        self.scale = scale
        self.low = scale.low
        self.high = scale.high
        self.borda_unordered_give_points = borda_unordered_give_points

    def __call__(self, x: object, candidates: set=None) -> BallotLevels:
        x = ConverterBallotGeneral()(x, candidates=None)
        if isinstance(x, BallotVeto):
            if x.candidate is None:
                return BallotLevels(dict(), candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
            return BallotLevels({c: self.low if c == x.candidate else self.high for c in x.candidates},
                                candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
        if isinstance(x, BallotOneName):  # Including Plurality
            if x.candidate is None:
                return BallotLevels(dict(), candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
            return BallotLevels({c: self.high if c == x.candidate else self.low for c in x.candidates},
                                candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
        if isinstance(x, BallotLevels):
            if not x.scale.is_bounded:
                if all([isinstance(v, numbers.Number) for v in x.values()]):
                    x_min, x_max = min(x.values()), max(x.values())
                    if x_min >= self.low and x_max <= self.high:
                        return BallotLevels(
                            x.as_dict, candidates=x.candidates,
                            scale=ScaleInterval(low=self.low, high=self.high)).restrict(candidates=candidates)
                    else:
                        x = BallotLevels(x.as_dict, candidates=x.candidates,
                                         scale=ScaleInterval(low=min(x.values()), high=max(x.values())))
                else:
                    x = BallotLevels(x.as_dict, candidates=x.candidates, scale=ScaleFromSet(set(x.values())))
            try:  # Interpret as a cardinal ballot
                return BallotLevels(
                    {c: self.low + my_division((self.high - self.low) * (v - x.scale.low), (x.scale.high - x.scale.low))
                     for c, v in x.items()},
                    candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
            except (TypeError, AttributeError):
                x_scale = x.scale
                if isinstance(x_scale, ScaleFromList):
                    return BallotLevels(
                        {c: self.low + my_division(
                            (self.high - self.low) * x_scale.as_dict[x[c]], (len(x_scale.levels) - 1))
                         for c, v in x.items()},
                        candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
        if isinstance(x, BallotOrder):
            borda = ScorerBorda(ballot=x, candidates=x.candidates,
                                unordered_give_points=self.borda_unordered_give_points).scores_
            score_max = len(x.candidates) - 1 if self.borda_unordered_give_points else len(x.candidates_in_b) - 1
            return BallotLevels(
                {c: self.low + my_division((self.high - self.low) * borda[c], score_max) for c in x.candidates_in_b},
                candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
        raise NotImplementedError
