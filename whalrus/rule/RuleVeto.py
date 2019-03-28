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
import logging
from whalrus.rule.RuleScoreNumAverage import RuleScoreNumAverage
from whalrus.scorer.Scorer import Scorer
from whalrus.scorer.ScorerVeto import ScorerVeto
from whalrus.converter_ballot.ConverterBallotToVeto import ConverterBallotToVeto
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.converter_ballot.ConverterBallot import ConverterBallot


class RuleVeto(RuleScoreNumAverage):
    """
    The veto rule.

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToVeto`.
    :param scorer: the default is :class:`ScorerVeto`.
    :param `**kwargs`: cf. parent class.

    >>> RuleVeto(['a', 'b', 'b', 'c', 'c']).winner_
    'a'
    """

    def __init__(self, *args, converter: ConverterBallot = None, scorer: Scorer = None, **kwargs):
        if converter is None:
            converter = ConverterBallotToVeto()
        if scorer is None:
            scorer = ScorerVeto()
        super().__init__(*args, converter=converter, scorer=scorer, **kwargs)

    def _check_profile(self, candidates: set) -> None:
        if any([len(b.candidates) > 1 and b.candidates != candidates for b in self.profile_converted_]):
            logging.warning('Some ballots do not have the same set of candidates as the whole election.')

    @cached_property
    def _gross_scores_and_weights_quicker_(self) -> dict:
        if not isinstance(self.scorer, ScorerVeto):
            return self._gross_scores_and_weights_
        # If it is a ScorerVeto, we have a quicker method.
        gross_scores = NiceDict({c: 0 for c in self.candidates_})
        total_weight = 0
        for ballot, weight, _ in self.profile_converted_.items():
            if ballot.candidate is None:
                if self.scorer.count_abstention:
                    total_weight += weight
                continue
            gross_scores[ballot.candidate] -= weight
            total_weight += weight
        weights = NiceDict({c: total_weight for c in self.candidates_})
        return {'gross_scores': gross_scores, 'weights': weights}

    @cached_property
    def gross_scores_(self) -> NiceDict:
        return self._gross_scores_and_weights_quicker_['gross_scores']

    @cached_property
    def weights_(self) -> NiceDict:
        return self._gross_scores_and_weights_quicker_['weights']
