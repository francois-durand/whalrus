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
from whalrus.scorer.Scorer import Scorer
from whalrus.scorer.ScorerBorda import ScorerBorda
from whalrus.rule.RuleScore import RuleScore
from whalrus.rule.RuleBucklinByRounds import RuleBucklinByRounds
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.utils.Utils import cached_property, NiceDict, my_division, convert_number
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.profile.Profile import Profile


class RuleBucklinInstant(RuleScore):
    """
    Bucklin's rule (instant version).

    :param `*args`: cf. parent class.
    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param scorer: a :class:`Scorer`. Default: :class:`ScorerBorda` with ``absent_give_points=True``,
        ``absent_receive_points=None``, ``unordered_give_points=True``, ``unordered_receive_points=False``.
    :param default_median: the default median of a candidate when it receives no score whatsoever.
    :param `**kwargs`: cf. parent class.

    >>> rule = RuleBucklinInstant(ballots=['a > b > c', 'b > a > c', 'c > a > b'])
    >>> rule.scores_
    {'a': (1, 3), 'b': (1, 2), 'c': (0, 3)}
    >>> rule.winner_
    'a'

    For each candidate, its median Borda score `m` is computed. Let `x` be the number of voters who give this
    candidate a Borda score that is greater or equal to `m`. Then the candidate's score is `(m, x)`. Scores are
    compared lexicographically.

    When preferences are strict orders, it is equivalent to say that:

        * The candidate with the lowest median rank is declared the winner.
        * If several candidates have the lowest median rank, this tie is broken by examining how many voters rank
          each of them with this rank or better.

    For another variant of Bucklin's rule, cf. :class:`RuleBucklinByRounds`. With the default settings,
    and when preferences are strict total orders, :class:`RuleBucklinByRounds` and :class:`RuleBucklinInstant` have
    the same winner (although not necessarily the same order over the candidates). Otherwise, the winners may differ:

    >>> profile = Profile(ballots=['a > b > c > d', 'b > a ~ d > c', 'c > a ~ d > b'],
    ...                   weights=[3, 3, 4])
    >>> rule_bucklin_by_rounds = RuleBucklinByRounds(profile)
    >>> rule_bucklin_by_rounds.detailed_scores_[0]
    {'a': Fraction(3, 10), 'b': Fraction(3, 10), 'c': Fraction(2, 5), 'd': 0}
    >>> rule_bucklin_by_rounds.detailed_scores_[1]
    {'a': Fraction(13, 20), 'b': Fraction(3, 5), 'c': Fraction(2, 5), 'd': Fraction(7, 20)}
    >>> rule_bucklin_by_rounds.winner_
    'a'
    >>> rule_bucklin_instant = RuleBucklinInstant(profile)
    >>> rule_bucklin_instant.scores_
    {'a': (Fraction(3, 2), 10), 'b': (2, 6), 'c': (1, 7), 'd': (Fraction(3, 2), 7)}
    >>> RuleBucklinInstant(profile).winner_
    'b'
    """

    def __init__(self, *args, converter: ConverterBallot = None, scorer: Scorer = None, default_median: object = 0,
                 **kwargs):
        # Default value
        if converter is None:
            converter = ConverterBallotToOrder()
        if scorer is None:
            scorer = ScorerBorda(absent_give_points=True, absent_receive_points=None,
                                 unordered_give_points=True, unordered_receive_points=False)
        # Parameters
        self.scorer = scorer
        self.default_median = default_median
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def scores_(self) -> NiceDict:
        levels_ = NiceDict({c: [] for c in self.candidates_})
        weights_ = NiceDict({c: [] for c in self.candidates_})
        for ballot, weight, voter in self.profile_converted_.items():
            for c, level in self.scorer(ballot=ballot, voter=voter, candidates=self.candidates_).scores_.items():
                levels_[c].append(level)
                weights_[c].append(weight)
        scores_ = NiceDict()
        for c in self.candidates_:
            if not levels_[c]:
                scores_[c] = (self.default_median, 0)
                continue
            indexes = self.scorer.scale.argsort(levels_[c])
            levels_[c] = [levels_[c][i] for i in indexes]
            weights_[c] = [weights_[c][i] for i in indexes]
            total_weight = sum(weights_[c])
            half_total_weight = my_division(total_weight, 2)
            cumulative_weight = 0
            median = None
            for i, weight in enumerate(weights_[c]):
                cumulative_weight += weight
                if cumulative_weight >= half_total_weight:
                    median = levels_[c][i]
                    break
            support = convert_number(sum([
                weights_[c][i] for i, level in enumerate(levels_[c]) if self.scorer.scale.ge(level, median)]))
            scores_[c] = (median, support)
        return scores_

    def compare_scores(self, one: tuple, another: tuple) -> int:
        if one == another:
            return 0
        if self.scorer.scale.lt(one[0], another[0]):
            return -1
        if self.scorer.scale.gt(one[0], another[0]):
            return 1
        return -1 if one[1] < another[1] else 1

    @cached_property
    def scores_as_floats_(self) -> NiceDict:
        """

        :return: :attr:`scores_`, converted to floats.
        """
        def my_float(x):
            try:
                return float(x)
            except ValueError:
                return x
        return NiceDict({c: (my_float(s), float(x)) for c, (s, x) in self.scores_.items()})
