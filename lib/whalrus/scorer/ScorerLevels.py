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
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.scorer.Scorer import Scorer


class ScorerLevels(Scorer):
    """
    A standard scorer for :class:``BallotLevel``.

    :param `*args`: cf. parent class.
    :param level_ungraded: the level of the scale used for ungraded candidates, or None.
    :param level_absent: the level of the scale used for absent candidates, or None.
    :param `**kwargs`: cf. parent class.

    In the most general syntax, firstly, you define the scorer:

    >>> scorer = ScorerLevels(level_absent=0)

    Secondly, you use it as a callable to load some particular arguments:

    >>> scorer(ballot=BallotLevels({'a': 10, 'b': 7, 'c': 3}), voter='Alice',
    ...        candidates={'a', 'b', 'c', 'd'})  # doctest:+ELLIPSIS
    <... object at ...>

    Finally, you can access the computed variables:

    >>> scorer.scores_
    {'a': 10, 'b': 7, 'c': 3, 'd': 0}

    Later, if you wish, you can load other arguments (ballot, etc) with the same scorer, and so on.

    Optionally, you can specify arguments as soon as the :class:`Scorer` object is initialized. This allows for
    "one-liners" such as:

    >>> ScorerLevels(ballot=BallotLevels({'a': 10, 'b': 7, 'c': 3}), voter='Alice',
    ...              candidates={'a', 'b', 'c', 'd'}, level_absent=0).scores_
    {'a': 10, 'b': 7, 'c': 3, 'd': 0}

    In the example below, candidates `a`, `b` and `c` are "ordered", `d` is "unordered", and `e` is "absent"
    in the ballot, meaning that `e` were not even available when the voter cast her ballot. The options of the
    scorer provide different ways to take these special cases into account:

    >>> ballot=BallotLevels({'a': 10, 'b': 7, 'c': 3}, candidates={'a', 'b', 'c', 'd'})
    >>> candidates_election = {'a', 'b', 'c', 'd', 'e'}
    >>> ScorerLevels(ballot, candidates=candidates_election).scores_
    {'a': 10, 'b': 7, 'c': 3}
    >>> ScorerLevels(ballot, candidates=candidates_election,
    ...              level_ungraded=-5).scores_
    {'a': 10, 'b': 7, 'c': 3, 'd': -5}
    >>> ScorerLevels(ballot, candidates=candidates_election,
    ...              level_ungraded=-5, level_absent=-10).scores_
    {'a': 10, 'b': 7, 'c': 3, 'd': -5, 'e': -10}
    """

    def __init__(self, *args, level_ungraded: object = None, level_absent: object = None, **kwargs):
        self.level_ungraded = level_ungraded
        self.level_absent = level_absent
        super().__init__(*args, **kwargs)

    @cached_property
    def scores_(self) -> NiceDict:
        scores = NiceDict(self.ballot_.as_dict.copy())
        if self.level_absent is not None:
            scores.update({c: self.level_absent for c in self.candidates_ - self.ballot_.candidates})
        if self.level_ungraded is not None:
            scores.update({c: self.level_ungraded for c in self.ballot_.candidates_not_in_b})
        return scores
