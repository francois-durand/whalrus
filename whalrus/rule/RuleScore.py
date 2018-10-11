from whalrus.rule.Rule import Rule
from whalrus.utils.Utils import cached_property
from numbers import Number


class RuleScore(Rule):
    """
    A voting rule with score.

    This is simply a voting rule where each candidate is assigned a numeric score, and the candidates with the best
    score are declared the cowinners.
    """

    @cached_property
    def scores_(self) -> dict:
        """
        The scores.

        :return: a dictionary that, to each candidate, assigns a score.
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
    def cowinners_(self):
        """
        Cowinners

        :return: the set of candidates with the best score.
        """
        return {k for k, v in self.scores_.items() if v == self.best_score_}
