from whalrus.rule.Rule import Rule
from whalrus.utils.Utils import cached_property, NiceDict, NiceSet
from numbers import Number


class RuleScore(Rule):
    """
    A voting rule with score.

    This is simply a voting rule where each candidate is assigned a numeric score, and the candidates with the best
    score are declared the cowinners.
    """

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The scores.

        :return: a :class:`NiceDict` that, to each candidate, assigns a score.
        """
        raise NotImplementedError

    @cached_property
    def best_score_(self) -> Number:
        """
        The best score.

        :return: the best score.
        """
        return max(self.scores_.values())

    @cached_property
    def worst_score_(self) -> Number:
        """
        The worst score.

        :return: the worst score.
        """
        return min(self.scores_.values())

    @cached_property
    def cowinners_(self):
        """
        Cowinners

        :return: the set of candidates with the best score.
        """
        return NiceSet({k for k, v in self.scores_.items() if v == self.best_score_})

    @cached_property
    def cotrailers_(self):
        """
        "Cotrailers"

        :return: the set of candidates with the worst score.
        """
        return NiceSet({k for k, v in self.scores_.items() if v == self.worst_score_})

    @cached_property
    def order_(self) -> list:
        """
        Result of the election as a (weak) order over the candidates.

        :return: a list of sets. The first set contains the candidates that have the best score, the second set
            contains those with the second best score, etc.
        """
        return [NiceSet(k for k in self.scores_.keys() if self.scores_[k] == v)
                for v in sorted(set(self.scores_.values()), reverse=True)]
