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
from whalrus.ballot.Ballot import Ballot


class ConverterBallot:
    """
    A ballot converter.

    A converter is a callable. Its input may have various formats. Its output must be a :class:`Ballot`, often of a
    specific subclass. For more information and examples, cf. :class:`ConverterBallotGeneral`.
    """
    def __call__(self, x: object, candidates: set=None) -> Ballot:
        raise NotImplementedError
