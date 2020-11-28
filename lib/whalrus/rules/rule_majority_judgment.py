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
from whalrus.scorers.scorer import Scorer
from whalrus.scorers.scorer_levels import ScorerLevels
from whalrus.scales.scale import Scale
from whalrus.scales.scale_from_list import ScaleFromList
from whalrus.rules.rule_score import RuleScore
from whalrus.converters_ballot.converter_ballot_to_levels import ConverterBallotToLevels
from whalrus.utils.utils import cached_property, NiceDict, my_division
from whalrus.converters_ballot.converter_ballot import ConverterBallot


class RuleMajorityJudgment(RuleScore):
    """
    Majority Judgment.

    Parameters
    ----------
    args
        Cf. parent class.
    converter : ConverterBallot
        Default: :class:`ConverterBallotToLevels`, with ``scale=scorer.scale``.
    scorer : Scorer
        Default: :class:`ScorerLevels`. Alternatively, you may provide an argument ``scale``. In that case, the scorer
        will be ``ScorerLevels(scale)``.
    default_median : object
        The median level that a candidate has when it receives absolutely no evaluation whatsoever.
    kwargs
        Cf. parent class.

    Examples
    --------
        >>> rule = RuleMajorityJudgment([{'a': 1, 'b': 1}, {'a': .5, 'b': .6},
        ...                              {'a': .5, 'b': .4}, {'a': .3, 'b': .2}])
        >>> rule.scores_as_floats_
        {'a': (0.5, -0.25, 0.25), 'b': (0.4, 0.5, -0.25)}
        >>> rule.winner_
        'a'

    For each candidate, its median evaluation `m` is computed. When a candidate has two medians (like candidate `b`
    in the above example, with .4 and .6), the lower value is considered. Let `p` (resp. `q`) denote the proportion of
    the voters who evaluate the candidate better (resp. worse) than its median. The score of the candidate is the tuple
    `(m, p, -q)` if `p > q`, and `(m, -q, p)` otherwise. Scores are compared lexicographically.

    For Majority Judgment, verbal evaluation are generally used. The following example is actually the same as
    above, but with verbal evaluations instead of grades:

        >>> rule = RuleMajorityJudgment([
        ...     {'a': 'Excellent', 'b': 'Excellent'}, {'a': 'Good', 'b': 'Very Good'},
        ...     {'a': 'Good', 'b': 'Acceptable'}, {'a': 'Poor', 'b': 'To Reject'}
        ... ], scale=ScaleFromList(['To Reject', 'Poor', 'Acceptable', 'Good', 'Very Good', 'Excellent']))
        >>> rule.scores_as_floats_
        {'a': ('Good', -0.25, 0.25), 'b': ('Acceptable', 0.5, -0.25)}
        >>> rule.winner_
        'a'

    By changing the ``scorer``, you may define a very different rule. The following one rewards the candidate with
    best median Borda score (with secondary criteria that are similar to Majority Judgment, i.e. the proportions of
    voters who give a candidate more / less than its median Borda score):

        >>> from whalrus.scorers.scorer_borda import ScorerBorda
        >>> from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
        >>> rule = RuleMajorityJudgment(scorer=ScorerBorda(), converter=ConverterBallotToOrder())
        >>> rule(['a > b ~ c > d', 'c > a > b > d']).scores_as_floats_
        {'a': (2.0, 0.5, 0.0), 'b': (1.0, 0.5, 0.0), 'c': (1.5, 0.5, 0.0), 'd': (0.0, 0.0, 0.0)}
        >>> rule.winner_
        'a'
    """

    def __init__(self, *args, converter: ConverterBallot = None, scorer: Scorer = None,
                 scale: Scale = None, default_median: object = None, **kwargs):
        # Default value
        if scorer is None:
            scorer = ScorerLevels(scale=scale)
        if converter is None:
            converter = ConverterBallotToLevels(scale=scorer.scale)
        # Parameters
        self.scorer = scorer
        self.default_median = default_median
        super().__init__(*args, converter=converter, **kwargs)

    @cached_property
    def scores_(self) -> NiceDict:
        """NiceDict: The scores. A :class:`NiceDict` of triples.
        """
        levels_ = NiceDict({c: [] for c in self.candidates_})
        weights_ = NiceDict({c: [] for c in self.candidates_})
        for ballot, weight, voter in self.profile_converted_.items():
            for c, level in self.scorer(ballot=ballot, voter=voter, candidates=self.candidates_).scores_.items():
                levels_[c].append(level)
                weights_[c].append(weight)
        scores_ = NiceDict()
        for c in self.candidates_:
            if not levels_[c]:
                scores_[c] = (self.default_median, 0, 0)
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
            p = sum([weights_[c][i] for i, level in enumerate(levels_[c]) if self.scorer.scale.gt(level, median)])
            q = sum([weights_[c][i] for i, level in enumerate(levels_[c]) if self.scorer.scale.lt(level, median)])
            if p > q:
                scores_[c] = (median, my_division(p, total_weight), -my_division(q, total_weight))
            else:
                scores_[c] = (median, -my_division(q, total_weight), my_division(p, total_weight))
        return scores_

    def compare_scores(self, one: tuple, another: tuple) -> int:
        if one == another:
            return 0
        if self.scorer.scale.lt(one[0], another[0]):
            return -1
        if self.scorer.scale.gt(one[0], another[0]):
            return 1
        return -1 if (one[1], one[2]) < (another[1], another[2]) else 1

    @cached_property
    def scores_as_floats_(self) -> NiceDict:
        """NiceDict: Scores as floats. It is the same as :attr:`scores_`, but converted to floats.
        """
        def my_float(x):
            try:
                return float(x)
            except ValueError:
                return x
        return NiceDict({c: (my_float(s), float(x), float(y)) for c, (s, x, y) in self.scores_.items()})
