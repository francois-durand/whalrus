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
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.converters_ballot.converter_ballot_to_levels_interval import ConverterBallotToLevelsInterval
from whalrus.ballots.ballot_veto import BallotVeto
from whalrus.ballots.ballot_plurality import BallotPlurality
from whalrus.ballots.ballot_one_name import BallotOneName
from whalrus.ballots.ballot_levels import BallotLevels
from whalrus.ballots.ballot_order import BallotOrder
from whalrus.scales.scale_interval import ScaleInterval
from whalrus.scales.scale_from_list import ScaleFromList
from whalrus.scales.scale_from_set import ScaleFromSet
from whalrus.scales.scale_range import ScaleRange


class ConverterBallotToLevelsRange(ConverterBallot):
    """
    Default converter to a :class:`BallotLevels` using a :class:`ScaleRange` (range of integers).

    This converter works essentially the same as :class:`ConverterBallotToLevelsInterval`, but it rounds the grades to
    the nearest integers.

    Parameters
    ----------
    scale : ScaleRange
        The scale.
    borda_unordered_give_points : bool
        When converting a :class:`BallotOrder` that is not a :class:`BallotLevels`, we use Borda scores (normalized to
        the interval [``scale.low``, ``scale.high``] and rounded). This parameter decides whether the unordered
        candidates of the ballot give points to the ordered candidates. Cf. :class:`ScorerBorda`.

    Examples
    --------
    Typical usages:

        >>> converter = ConverterBallotToLevelsRange(scale=ScaleRange(low=0, high=10))
        >>> b = BallotLevels({'a': 1, 'b': .4}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(-1, 1))
        >>> converter(b).as_dict
        {'a': 10, 'b': 7}
        >>> b = BallotLevels({'a': 5, 'b': 4}, candidates={'a', 'b', 'c'}, scale=ScaleRange(0, 5))
        >>> converter(b).as_dict
        {'a': 10, 'b': 8}
        >>> b = BallotLevels({'a': 4, 'b': 0}, candidates={'a', 'b', 'c'}, scale=ScaleFromSet({-1, 0, 4}))
        >>> converter(b).as_dict
        {'a': 10, 'b': 2}
        >>> b = BallotLevels(
        ...     {'a': 'Excellent', 'b': 'Very Good'}, candidates={'a', 'b', 'c'},
        ...     scale=ScaleFromList(['Bad', 'Medium', 'Good', 'Very Good', 'Great', 'Excellent']))
        >>> converter(b).as_dict
        {'a': 10, 'b': 6}
        >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'})).as_dict
        {'a': 10, 'b': 0, 'c': 0}
        >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'})).as_dict
        {'a': 10, 'b': 0, 'c': 0}
        >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'})).as_dict
        {'a': 0, 'b': 10, 'c': 10}
        >>> converter('a > b > c').as_dict
        {'a': 10, 'b': 5, 'c': 0}

    Options for converting ordered ballots:

        >>> b = BallotOrder('a > b > c', candidates={'a', 'b', 'c', 'd', 'e', 'f'})
        >>> converter = ConverterBallotToLevelsRange(scale=ScaleRange(low=0, high=10),
        ...                                          borda_unordered_give_points=False)
        >>> converter(b).as_dict
        {'a': 10, 'b': 5, 'c': 0}
        >>> converter = ConverterBallotToLevelsRange(scale=ScaleRange(low=0, high=10),
        ...                                          borda_unordered_give_points=True)
        >>> converter(b).as_dict
        {'a': 10, 'b': 8, 'c': 6}
    """

    def __init__(self, scale: ScaleRange = ScaleRange(0, 1), borda_unordered_give_points: bool = True):
        self.scale = scale
        self.low = scale.low
        self.high = scale.high
        self.borda_unordered_give_points = borda_unordered_give_points

    def __call__(self, x: object, candidates: set = None) -> BallotLevels:
        x = ConverterBallotToLevelsInterval(
            scale=ScaleInterval(low=self.low, high=self.high),
            borda_unordered_give_points=self.borda_unordered_give_points
        )(x, candidates=None)
        return BallotLevels({c: round(v) for c, v in x.items()},
                            candidates=x.candidates, scale=self.scale).restrict(candidates=candidates)
