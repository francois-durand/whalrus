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
from whalrus.scales.scale_range import ScaleRange
from whalrus.rules.rule_range_voting import RuleRangeVoting
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from whalrus.converters_ballot.converter_ballot_to_grades import ConverterBallotToGrades


class RuleApproval(RuleRangeVoting):
    """
    Approval voting.

    Parameters
    ----------
    args
        Cf. parent class.
    converter : ConverterBallot
        Default: ``ConverterBallotToGrades(scale=ScaleRange(0, 1))``. This is the only difference with the parent class
        :class:`RuleRangeVoting`.
    kwargs
        Cf. parent class.

    Examples
    --------
        >>> RuleApproval([{'a': 1, 'b': 0, 'c': 0}, {'a': 1, 'b': 1, 'c': 0}]).gross_scores_
        {'a': 2, 'b': 1, 'c': 0}
    """

    def __init__(self, *args, converter: ConverterBallot = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToGrades(scale=ScaleRange(0, 1))
        super().__init__(*args, converter=converter, **kwargs)
