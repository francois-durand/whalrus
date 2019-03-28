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
from whalrus.utils.Utils import cached_property
from whalrus.rule.Rule import Rule
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.rule.RulePlurality import RulePlurality
from whalrus.elimination.Elimination import Elimination
from whalrus.elimination.EliminationLast import EliminationLast
from whalrus.elimination.EliminationBelowAverage import EliminationBelowAverage
from typing import Union
from copy import deepcopy
from itertools import chain


class RuleSequentialElimination(Rule):
    # noinspection PyUnresolvedReferences
    """
    A rule by sequential elimination (such as :class:`RuleTwoRound`).

    :param `*args`: cf. parent class.
    :param rules: a list of rules, one for each round. Unlike for :class:`RuleIteratedElimination`, different rounds
        may use different voting rules.
    :param eliminations: a list of elimination algorithms, one for each round except the last one.
    :param propagate_tie_break: if True (default), then the tie-breaking rule of this object is also used for the
        base rules. Cf. :class:`RuleIteratedElimination` for more explanation on this parameter.
    :param `**kwargs`: cf. parent class.

    >>> rule = RuleSequentialElimination(
    ...     ['a > b > c > d > e', 'b > c > d > e > a'], weights=[2, 1],
    ...     rules=[RuleBorda(), RulePlurality(), RulePlurality()],
    ...     eliminations=[EliminationBelowAverage(), EliminationLast(k=1)])
    >>> rule.elimination_rounds_[0].rule_.gross_scores_
    {'a': 8, 'b': 10, 'c': 7, 'd': 4, 'e': 1}
    >>> rule.elimination_rounds_[1].rule_.gross_scores_
    {'a': 2, 'b': 1, 'c': 0}
    >>> rule.final_round_.gross_scores_
    {'a': 2, 'b': 1}

    If ``rules`` is not a list, the number of rounds is inferred from ``eliminations``. An application of this is to
    define the two-round system:

    >>> rule = RuleSequentialElimination(
    ...     ['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'], weights=[2, 2, 1],
    ...     rules=RulePlurality(), eliminations=[EliminationLast(k=-2)])
    >>> rule.elimination_rounds_[0].rule_.gross_scores_
    {'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 0}
    >>> rule.final_round_.gross_scores_
    {'a': 3, 'b': 2}

    Note: there exists a shortcut for the above rule in particular, the class :class:`RuleTwoRound`.

    Similarly, if ``elimination`` is not a list, the number of rounds is deduced from ``rules``:

    >>> rule = RuleSequentialElimination(
    ...     ['a > b > c > d > e', 'b > a > c > d > e'], weights=[2, 1],
    ...     rules=[RuleBorda(), RuleBorda(), RulePlurality()], eliminations=EliminationLast(k=1))
    >>> rule.elimination_rounds_[0].rule_.gross_scores_
    {'a': 11, 'b': 10, 'c': 6, 'd': 3, 'e': 0}
    >>> rule.elimination_rounds_[1].rule_.gross_scores_
    {'a': 8, 'b': 7, 'c': 3, 'd': 0}
    >>> rule.final_round_.gross_scores_
    {'a': 2, 'b': 1, 'c': 0}
    """

    def __init__(self, *args, rules: Union[list, Rule] = None, eliminations: Union[list, Elimination] = None,
                 propagate_tie_break=True, **kwargs):
        # Default values
        if eliminations is None:
            eliminations = EliminationLast(k=1)
        # Deal with the polymorphism of the definition
        if isinstance(rules, list):
            n_rounds = len(rules)
        elif isinstance(eliminations, list):
            n_rounds = len(eliminations) + 1
        else:
            n_rounds = 1
        if isinstance(rules, Rule):
            rules.delete_cache()
            rules = [deepcopy(rules) for _ in range(n_rounds)]
        if isinstance(eliminations, Elimination):
            eliminations.delete_cache()
            eliminations = [deepcopy(eliminations) for _ in range(n_rounds - 1)]
        # Record variables and initialize
        self.rules = rules
        self.eliminations = eliminations
        self.propagate_tie_break = propagate_tie_break
        super().__init__(*args, **kwargs)

    def _check_profile(self, candidates: set) -> None:
        # We delegate this task to the base rules.
        pass

    @cached_property
    def rounds_(self) -> list:
        # noinspection PyUnresolvedReferences
        """
        The rounds.

        :return: a list. All rounds but the last one are :class:`Elimination` objects. The last one is a :class:`Rule`
            object.

        Note that in some cases, there may be fewer actual rounds than declared in the definition of the rule:

        >>> rule = RuleSequentialElimination(
        ...     ['a > b > c > d', 'a > c > d > b', 'a > d > b > c'],
        ...     rules=[RuleBorda(), RulePlurality(), RulePlurality()],
        ...     eliminations=[EliminationBelowAverage(), EliminationLast(k=1)])
        >>> len(rule.rounds_)
        2
        >>> rule.elimination_rounds_[0].rule_.gross_scores_
        {'a': 9, 'b': 3, 'c': 3, 'd': 3}
        >>> rule.final_round_.gross_scores_
        {'a': 3}
        """
        rounds = []
        candidates = self.candidates_
        for i, elimination in enumerate(self.eliminations):
            rule = self.rules[i]
            if self.propagate_tie_break:
                rule.tie_break = self.tie_break
            rule(ballots=self.profile_converted_, candidates=candidates)
            elimination(rule=rule)
            candidates = elimination.qualified_
            if candidates:
                rounds.append(elimination)
            else:
                rounds.append(rule)
                break
        else:
            rule = self.rules[-1]
            if self.propagate_tie_break:
                rule.tie_break = self.tie_break
            rule(ballots=self.profile_converted_, candidates=candidates)
            rounds.append(rule)
        return rounds

    @cached_property
    def elimination_rounds_(self) -> list:
        """
        The elimination rounds.

        :return: a list of :class:`Elimination` objects. All rounds except the last one.
        """
        return self.rounds_[:-1]

    @cached_property
    def final_round_(self) -> Rule:
        """
        The final round.

        :return: a :class:`Rule` object. The last round, which decides the winner of the election.
        """
        return self.rounds_[-1]

    @cached_property
    def order_(self) -> list:
        return (self.final_round_.order_ +
                list(chain(*[elimination.eliminated_order_ for elimination in self.elimination_rounds_[::-1]])))
