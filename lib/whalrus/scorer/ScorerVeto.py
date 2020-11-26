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
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.scorer.Scorer import Scorer


class ScorerVeto(Scorer):
    """
    A Veto scorer for :class:`BallotVeto`.

    :param `*args`: cf. parent class.
    :param count_abstention: if False (default), then an abstention grants no score at all. If True, then an
        abstention gives 0 point to each candidate (cf. below).
    :param `**kwargs`: cf. parent class.

    Typical usage:

    >>> ScorerVeto(BallotVeto('a'), candidates={'a', 'b', 'c'}).scores_
    {'a': -1, 'b': 0, 'c': 0}

    Using the option ``count_abstention``:

    >>> ScorerVeto(BallotVeto(None), candidates={'a', 'b', 'c'}).scores_
    {}
    >>> ScorerVeto(BallotVeto(None), candidates={'a', 'b', 'c'},
    ...                 count_abstention=True).scores_
    {'a': 0, 'b': 0, 'c': 0}
    """

    def __init__(self, *args, count_abstention: bool = False, **kwargs):
        self.count_abstention = count_abstention
        super().__init__(*args, **kwargs)

    @cached_property
    def scores_(self) -> NiceDict:
        if self.ballot_.candidate is None:
            if self.count_abstention:
                return NiceDict({c: 0 for c in self.candidates_})
            else:
                return NiceDict()
        scores = NiceDict({c: 0 for c in self.candidates_})
        scores[self.ballot_.candidate] = -1
        return scores
