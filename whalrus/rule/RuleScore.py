from whalrus.rule.Rule import Rule
from whalrus.utils.Utils import cached_property, NiceDict, NiceSet
from functools import cmp_to_key


class RuleScore(Rule):
    """
    A voting rule with score (which may not be a number).

    Each candidate is assigned a score (not necessarily a number), and the candidates with the best score (in some
    sense) are declared the cowinners.
    """

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The scores.

        :return: a :class:`NiceDict` that, to each candidate, assigns a score (non necessarily numeric).
        """
        raise NotImplementedError

    def compare_scores(self, one: object, another: object) -> int:
        """
        Compare two scores.

        :param one: a score.
        :param another: a score.
        :return: 0 if they are equal, a positive number if ``one`` is greater than ``another``, a negative number
            otherwise.
        """
        raise NotImplementedError

    @cached_property
    def best_score_(self) -> object:
        """
        The best score.

        :return: the best score.
        """
        return max(self.scores_.values(), key=cmp_to_key(self.compare_scores))

    @cached_property
    def worst_score_(self) -> object:
        """
        The worst score.

        :return: the worst score.
        """
        return min(self.scores_.values(), key=cmp_to_key(self.compare_scores))

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
                for v in sorted(set(self.scores_.values()), key=cmp_to_key(self.compare_scores), reverse=True)]
