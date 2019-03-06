from whalrus.utils.Utils import cached_property, NiceSet
from whalrus.rule.Rule import Rule
from whalrus.elimination.Elimination import Elimination
from whalrus.rule.RulePlurality import RulePlurality
from whalrus.priority.Priority import Priority


class EliminationLast(Elimination):
    """
    Elimination of the last candidates in an election

    :param k: an nonzero integer. The number of eliminated candidates. If this number is negative, then
        ``len(rule.candidates_) - abs(k)`` candidates are eliminated, i.e. ``abs(k)`` candidates are qualified.

    Typical usage with ``k = 1`` (for :class:`RuleIRV`):

    >>> rule = RulePlurality(ballots=['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'e'], tie_break=Priority.ASCENDING)
    >>> EliminationLast(rule=rule, k=1).eliminated_
    {'e'}

    Typical usage with ``k = -2`` (for :class:`RuleTwoRound`):

    >>> rule = RulePlurality(ballots=['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'e'], tie_break=Priority.ASCENDING)
    >>> EliminationLast(rule=rule, k=-2).qualified_
    {'a', 'b'}

    Order of elimination:

    >>> rule = RulePlurality(ballots=['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'e'], tie_break=Priority.ASCENDING)
    >>> EliminationLast(rule=rule, k=-2).eliminated_order_
    [{'c'}, {'d', 'e'}]

    There must always be at least one qualified candidate. If it is not possible to eliminate (case ``k > 0``)  or keep
    (case ``k < 0``) as many candidates as required, then everybody is eliminated:

    >>> rule = RulePlurality(ballots=['a'])
    >>> EliminationLast(rule=rule, k=1).qualified_
    {}
    >>> EliminationLast(rule=rule, k=-2).qualified_
    {}
    """

    def __init__(self, rule: Rule = None, k: int = 1):
        self.k = k
        super().__init__(rule)

    @cached_property
    def eliminated_order_(self):
        if self.k > 0:
            n_wanted = self.k
        else:
            n_wanted = self.rule_.n_candidates_ + self.k
        if n_wanted <= 0 or n_wanted >= self.rule_.n_candidates_:
            return self.rule_.order_
        worst_first = []
        for tie_class in self.rule_.order_[::-1]:
            size_class = len(tie_class)
            if size_class <= n_wanted:
                worst_first.append(tie_class)
                n_wanted -= size_class
                if n_wanted == 0:
                    break
            else:
                worst_first.append(NiceSet(self.rule_.tie_break.sort(tie_class)[-1:-1 - n_wanted:-1]))
                break
        return worst_first[::-1]
