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
from whalrus.scorer.ScorerBucklin import ScorerBucklin
from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property, NiceDict, my_division
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from fractions import Fraction


class RuleBucklinByRounds(RuleScoreNum):
    """
    Bucklin's rule (round by round version).

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param scorer: the default is :class:`ScorerBucklin`.
    :param `**kwargs`: cf. parent class.

    >>> rule = RuleBucklinByRounds(['a > b > c > d', 'b > a > c > d',
    ...                             'c > a > b > d', 'd > a > b > c'])
    >>> rule.detailed_scores_[0]
    {'a': Fraction(1, 4), 'b': Fraction(1, 4), 'c': Fraction(1, 4), 'd': Fraction(1, 4)}
    >>> rule.detailed_scores_[1]
    {'a': 1, 'b': Fraction(1, 2), 'c': Fraction(1, 4), 'd': Fraction(1, 4)}
    >>> rule.n_rounds_
    2
    >>> rule.scores_
    {'a': 1, 'b': Fraction(1, 2), 'c': Fraction(1, 4), 'd': Fraction(1, 4)}
    >>> rule.winner_
    'a'

    During the first round, a candidate's score is the proportion of voters who rank it first. During the second
    round, its score is the proportion of voters who rank it first or second. Etc. More precisely, at each round, the
    ``scorer`` is used with ``k`` equal to the round number; cf. :class:`ScorerBucklin`.

    For another variant of Bucklin's rule, cf. :class:`RuleBucklinInstant`.
    """

    def __init__(self, *args, converter: ConverterBallot = None, scorer: ScorerBucklin = None, **kwargs):
        # Default value
        if converter is None:
            converter = ConverterBallotToOrder()
        if scorer is None:
            scorer = ScorerBucklin()
        # Parameters
        self.scorer = scorer
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def detailed_scores_(self) -> list:
        """
        Detailed scores.

        :return: a list of :class:`NiceDict`. The first dictionary gives the scores of the first round, etc.
        """
        n_candidates = len(self.candidates_)
        detailed_scores = []
        for k in range(1, n_candidates + 1):
            self.scorer.k = k
            gross_scores = NiceDict({c: 0 for c in self.candidates_})
            weights = NiceDict({c: 0 for c in self.candidates_})
            for ballot, weight, voter in self.profile_converted_.items():
                for c, value in self.scorer(ballot=ballot, voter=voter, candidates=self.candidates_).scores_.items():
                    gross_scores[c] += weight * value
                    weights[c] += weight
            scores = NiceDict({c: my_division(score, weights[c], divide_by_zero=0)
                               for c, score in gross_scores.items()})
            detailed_scores.append(scores)
            if max(scores.values()) > Fraction(1, 2):
                break
        return detailed_scores

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The scores.

        :return: a :class:`NiceDict`. For each candidate, it gives its score during the final round, i.e. the first
            round where at least one candidate has a score above 1 / 2.
        """
        return self.detailed_scores_[-1]

    @cached_property
    def n_rounds_(self) -> int:
        """
        Number of rounds

        :return: the number of rounds.
        """
        return len(self.detailed_scores_)

    # Conversion to floats
    # --------------------

    @cached_property
    def detailed_scores_as_floats_(self) -> list:
        """
        Detailed scores, as floats.

        :return: :attr:`detailed_scores_`, converted to floats.
        """
        return [NiceDict({c: float(v) for c, v in counting_round.items()}) for counting_round in self.detailed_scores_]
