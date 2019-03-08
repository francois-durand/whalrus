from whalrus.rule.RuleScore import RuleScore
from whalrus.utils.Utils import cached_property, NiceDict, NiceSet
from numbers import Number


class RuleScoreNum(RuleScore):
    """
    A voting rule with a numeric score.

    This is simply a voting rule where each candidate is assigned a numeric score, and the candidates with the best
    score are declared the cowinners.
    """

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The scores.

        :return: a :class:`NiceDict` that, to each candidate, assigns a numeric score.
        """
        raise NotImplementedError

    def compare_scores(self, one: Number, another: Number) -> int:
        if one == another:
            return 0
        return -1 if one < another else 1

    @cached_property
    def best_score_(self) -> Number:
        return max(self.scores_.values())

    @cached_property
    def worst_score_(self) -> Number:
        return min(self.scores_.values())

    @cached_property
    def average_score_(self) -> Number:
        """
        The average score.

        :return: the average score.
        """
        return sum(self.scores_.values()) / self.n_candidates_

    @cached_property
    def order_(self) -> list:
        return [NiceSet(k for k in self.scores_.keys() if self.scores_[k] == v)
                for v in sorted(set(self.scores_.values()), reverse=True)]
