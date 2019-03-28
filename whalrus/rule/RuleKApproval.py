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
from whalrus.rule.RuleScorePositional import RuleScorePositional


class RuleKApproval(RuleScorePositional):
    """
    K-Approval

    :param `*args`: cf. parent class.
    :param k: the number of approved candidates.
    :param `**kwargs`: cf. parent class.

    The ``k`` top candidates in a ballot receive 1 point, and the other candidates receive 0 point.

    >>> RuleKApproval(['a > b > c', 'b > c > a'], k=2).gross_scores_
    {'a': 1, 'b': 2, 'c': 1}
    """

    def __init__(self, *args, k: int = 1, **kwargs):
        super().__init__(*args, points_scheme=[1] * k, **kwargs)
