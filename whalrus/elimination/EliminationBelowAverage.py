from whalrus.utils.Utils import cached_property
from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.elimination.Elimination import Elimination
from whalrus.rule.RulePlurality import RulePlurality


class EliminationBelowAverage(Elimination):
    """
    Elimination of the candidates whose score is lower than the average score

    :param strict: if True (resp. False), then eliminate the candidates whose score is strictly lower than
        (resp. lower or equal to) the average.

    >>> rule = RulePlurality(ballots=['a', 'b', 'c'],weights=[3, 2, 1])
    >>> rule.scores_
    {'a': 3, 'b': 2, 'c': 1}
    >>> EliminationBelowAverage(rule=rule).eliminated_
    {'c'}
    >>> EliminationBelowAverage(rule=rule, strict=False).eliminated_
    {'b', 'c'}

    If no candidates should be eliminated (which may happen only if ``strict`` is True), then all candidates are
    eliminated.

    >>> rule = RulePlurality(ballots=['a', 'b'])
    >>> rule.scores_
    {'a': 1, 'b': 1}
    >>> EliminationBelowAverage(rule=rule).eliminated_
    {'a', 'b'}
    """

    def __init__(self, rule: RuleScoreNum = None, strict=True):
        self.strict = strict
        super().__init__(rule)

    @cached_property
    def eliminated_order_(self):
        if self.rule_.best_score_ == self.rule_.worst_score_:
            return self.rule_.order_
        worst_first = []
        for tie_class in self.rule_.order_[::-1]:
            some_candidate = list(tie_class)[0]
            score = self.rule_.scores_[some_candidate]
            if score < self.rule_.average_score_ or (not self.strict and score == self.rule_.average_score_):
                worst_first.append(tie_class)
            else:
                break
        return worst_first[::-1]
