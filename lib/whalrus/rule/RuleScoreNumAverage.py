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
from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.scorer.Scorer import Scorer
from whalrus.utils.Utils import cached_property, NiceDict, my_division
from numbers import Number


class RuleScoreNumAverage(RuleScoreNum):
    """
    A voting rule where each candidate's score is an average of the scores provided by the ballots.

    :param `*args`: cf. parent class.
    :param scorer: the :class:`Scorer`. For each ballot, it is in charge of computing its contribution to each
        candidate's score.
    :param default_average: the default average score of a candidate when it receives no score whatsoever. It may
        happen, for example, if all voters abstain about this candidate. This avoids a division by zero when
        computing this candidate's average score.
    :param `**kwargs`: cf. parent class.

    Cf. :class:`RuleRangeVoting` for some examples.
    """

    def __init__(self, *args, scorer: Scorer = None, default_average: Number = 0, **kwargs):
        self.scorer = scorer
        self.default_average = default_average
        super().__init__(*args, **kwargs)

    @cached_property
    def _gross_scores_and_weights_(self) -> dict:
        gross_scores = NiceDict({c: 0 for c in self.candidates_})
        weights = NiceDict({c: 0 for c in self.candidates_})
        for ballot, weight, voter in self.profile_converted_.items():
            for c, value in self.scorer(ballot=ballot, voter=voter, candidates=self.candidates_).scores_.items():
                gross_scores[c] += weight * value
                weights[c] += weight
        return {'gross_scores': gross_scores, 'weights': weights}

    @cached_property
    def gross_scores_(self) -> NiceDict:
        """
        The gross scores of the candidates.

        :return: a :class:`NiceDict`. For each candidate, it gives the sum of its scores, multiplied by the weights
            of the corresponding voters. This is the numerator in the candidate's average score.
        """
        return self._gross_scores_and_weights_['gross_scores']

    @cached_property
    def weights_(self) -> NiceDict:
        """
        The weights used for the candidates.

        :return: a :class:`NiceDict`. For each candidate, it gives the total weight for this candidate, i.e. the total
            weight of all voters who assign a score to this candidate. This is the denominator in the candidate's
            average score.
        """
        return self._gross_scores_and_weights_['weights']

    @cached_property
    def scores_(self) -> NiceDict:
        return NiceDict({c: my_division(score, self.weights_[c], divide_by_zero=self.default_average)
                         for c, score in self.gross_scores_.items()})

    # Conversion to floats
    # --------------------

    @cached_property
    def gross_scores_as_floats_(self) -> NiceDict:
        """
        Gross scores as floats.

        :return: :attr:`gross_scores_` converted to floats.
        """
        return NiceDict({c: float(v) for c, v in self.gross_scores_.items()})

    @cached_property
    def weights_as_floats_(self) -> NiceDict:
        """
        Weights as floats.

        :return: :attr:`weights_` converted to floats.
        """
        return NiceDict({c: float(v) for c, v in self.weights_.items()})
