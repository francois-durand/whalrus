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
from whalrus.utils.utils import cached_property, NiceSet
from whalrus.selections.selection import Selection
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.priorities.priority import Priority


class SelectionFirst(Selection):
    """
    

    Parameters
    ----------
    args
        Cf. parent class.
    k : int
        A nonzero integer. The number of eliminated candidates. If this number is negative, then
        ``len(rule.candidates_) - abs(k)`` candidates are eliminated, i.e. ``abs(k)`` candidates are qualified.
    kwargs`
        Cf. parent class.

    Examples
    --------
    In the most general syntax, firstly, you define the elimination method:

        >>> selection = SelectionFirst(k=1)

    Secondly, you use it as a callable to load a particular election (rule, profile, candidates):

        >>> rule = RulePlurality(ballots=['a','a', 'a', 'b', 'b', 'c'])
        >>> selection(rule)  # doctest:+ELLIPSIS
        <... object at ...>

    Finally, you can access the computed variables:

        >>> selection.selected_
        {'a'}

    Later, if you wish, you can load another election with the same selection method, and so on.

    Optionally, you can specify an election (rule, profile, candidates) as soon as the :class:`Selection` object is
    initialized. This allows for one-liners such as:

        >>> SelectionFirst(rule=RulePlurality(ballots=['a','a', 'a', 'b', 'b', 'c']), k=1).selected_
        {'a'}

    Typical usage with ``k = 1`` (e.g. for :class:`RuleIRV`):

        >>> rule = RulePlurality(ballots=['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'e'],
        ...                      tie_break=Priority.ASCENDING)
        >>> SelectionFirst(rule=rule, k=1).selected_
        {'a'}

    Typical usage with ``k = -2`` (e.g. for :class:`RuleTwoRound`):

        >>> rule = RulePlurality(ballots=['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'e'],
        ...                      tie_break=Priority.ASCENDING)
        >>> SelectionFirst(rule=rule, k=-2).remaining_
        {'d', 'e'}

    Order of selection:

        >>> rule = RulePlurality(ballots=['a', 'a', 'a', 'b', 'b', 'c', 'c', 'd', 'e'],
        ...                      tie_break=Priority.ASCENDING)
        >>> SelectionFirst(rule=rule, k=-2).selected_order_
        [{'b', 'c'}, {'a'}]

    There must always be at least one selection candidate. If it is not possible to select (case ``k`` > 0)  or keep
    (case ``k`` < 0) as many candidates as required, then everybody is selected:

        >>> rule = RulePlurality(ballots=['a'])
        >>> SelectionFirst(rule=rule, k=1).selected_
        {'a'}
        >>> SelectionFirst(rule=rule, k=-2).selected_
        {'a'}
    """

    def __init__(self, *args, k: int = 1, **kwargs):
        self.k = k
        super().__init__(*args, **kwargs)

    @cached_property
    def selected_order_(self):
        if self.k > 0:
            n_wanted = self.k
        else:
            n_wanted = self.rule_.n_candidates_ + self.k
        if n_wanted <= 0 or n_wanted >= self.rule_.n_candidates_:
            return self.rule_.order_
        best_first = []
        for tie_class in self.rule_.order_:
            size_class = len(tie_class)
            if size_class <= n_wanted:
                best_first.append(tie_class)
                n_wanted -= size_class
                if n_wanted == 0:
                    break
            else:
                best_first.append(NiceSet(self.rule_.tie_break.sort(tie_class)[:n_wanted]))
                break
        return best_first[::-1]



