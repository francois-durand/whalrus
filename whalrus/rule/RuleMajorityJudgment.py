from whalrus.scale.Scale import Scale
from whalrus.scale.ScaleFromList import ScaleFromList
from whalrus.scale.ScaleInterval import ScaleInterval
from whalrus.rule.RuleScore import RuleScore
from whalrus.converter_ballot.ConverterBallotToLevels import ConverterBallotToLevels
from whalrus.priority.Priority import Priority
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.profile.Profile import Profile
from typing import Union


class RuleMajorityJudgment(RuleScore):
    """
    Majority Judgment.

    :param default_converter: the default is ``ConverterBallotToLevels(scale)``.
    :param scale: the scale. Default: ``ScaleInterval(0., 1.)``.
    :param level_ungraded: the default level when a ballot does not evaluate a candidate (partial or total abstention).
        If None (default), then the score is computed only over non-abstainers (cf. examples below).
    :param level_absent: the default level when a voter did not even see the candidate (i.e. it is not in its
        attribute ``candidates``). If None (default), then the score is computed only over non-abstainers (cf.
        examples below).
    :param default_median: the median level that a candidate has when it receives absolutely no evaluation whatsoever.

    Cf. :class:`RulePlurality` and :class:`Rule` for the general syntax.

    >>> rule = RuleMajorityJudgment([{'a': 1., 'b': 1.}, {'a': .5, 'b': .6}, {'a': .5, 'b': .4}, {'a': .3, 'b': .2}])
    >>> rule.scores_
    {'a': (0.5, -0.25, 0.25), 'b': (0.4, 0.5, -0.25)}
    >>> rule.winner_
    'a'

    For each candidate, its median evaluation is computed. When a candidate has two medians (as ``b`` above,
    with .4 and .6), the lower value is considered. Then ``p`` (resp. ``q``) is the proportion of the voters who
    evaluate the candidate better (resp. worse) than its median. The score of the candidate is the tuple
    ``(median, p, -q)`` if ``p > q``, and ``(median, -q, p)`` otherwise. Finally, scores are compared lexicographically.

    For Majority Judgment, verbal evaluation are generally used. The following example is actually the same as
    above, but with verbal evaluations instead of grades:

    >>> rule = RuleMajorityJudgment(ballots=[
    ...     {'a': 'Excellent', 'b': 'Excellent'}, {'a': 'Good', 'b': 'Very Good'},
    ...     {'a': 'Good', 'b': 'Acceptable'}, {'a': 'Poor', 'b': 'To Reject'}
    ... ], scale=ScaleFromList(['To Reject', 'Poor', 'Acceptable', 'Good', 'Very Good', 'Excellent']))
    >>> rule.scores_
    {'a': ('Good', -0.25, 0.25), 'b': ('Acceptable', 0.5, -0.25)}
    >>> rule.winner_
    'a'

    For more insight about the options, cf. :class:`RuleRangeVoting`.
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, default_converter: ConverterBallot = None,
                 scale: Scale = None,
                 level_ungraded: object = None,
                 level_absent: object = None,
                 default_median: object = None):
        if scale is None:
            scale = ScaleInterval(0., 1.)
        if default_converter is None:
            default_converter = ConverterBallotToLevels(scale=scale)
        self.scale = scale
        self.level_ungraded = level_ungraded
        self.level_absent = level_absent
        self.default_median = default_median
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter
        )

    @cached_property
    def scores_(self) -> NiceDict:
        levels_ = NiceDict({c: [] for c in self.candidates_})
        weights_ = NiceDict({c: [] for c in self.candidates_})
        for ballot, weight, _ in self.profile_converted_.items():
            if self.level_absent is not None:
                for c in (self.candidates_ - ballot.candidates):
                    levels_[c].append(self.level_absent)
                    weights_[c].append(weight)
            if self.level_ungraded is not None:
                for c in ballot.candidates_not_in_b:
                    levels_[c].append(self.level_ungraded)
                    weights_[c].append(weight)
            for c, level in ballot.items():
                levels_[c].append(level)
                weights_[c].append(weight)
        scores_ = NiceDict()
        for c in self.candidates_:
            if not levels_[c]:
                scores_[c] = (self.default_median, 0, 0)
                continue
            indexes = self.scale.argsort(levels_[c])
            levels_[c] = [levels_[c][i] for i in indexes]
            weights_[c] = [weights_[c][i] for i in indexes]
            total_weight = sum(weights_[c])
            half_total_weight = total_weight / 2
            cumulative_weight = 0
            median = None
            for i, weight in enumerate(weights_[c]):
                cumulative_weight += weight
                if cumulative_weight >= half_total_weight:
                    median = levels_[c][i]
                    break
            p = sum([weights_[c][i] for i, level in enumerate(levels_[c]) if self.scale.gt(level, median)])
            q = sum([weights_[c][i] for i, level in enumerate(levels_[c]) if self.scale.lt(level, median)])
            if p > q:
                scores_[c] = (median, p / total_weight, -q / total_weight)
            else:
                scores_[c] = (median, -q / total_weight, p / total_weight)
        return scores_

    def compare_scores(self, one: tuple, another: tuple) -> int:
        if one == another:
            return 0
        if self.scale.lt(one[0], another[0]):
            return -1
        if self.scale.gt(one[0], another[0]):
            return 1
        return -1 if (one[1], one[2]) < (another[1], another[2]) else 1
