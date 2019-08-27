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
from whalrus.utils.Utils import cached_property, NiceSet, NiceFrozenSet
from whalrus.rule_committee.RuleCommittee import RuleCommittee


class Rule(RuleCommittee):
    """
    A voting rule, designed to elect a single winner.

    This class is a subclass of :class:`RuleCommittee` in the sense that it always elects a committee of size 1.
    Cf. parent class :class:`RuleCommittee` for the documentation on parameters and instance variables.

    Cf. :class:`RulePlurality` for some examples.
    """

    @cached_property
    def cowinners_(self) -> NiceSet:
        """
        Cowinners of the election.

        :return: the set of cowinners, i.e. the candidates that fare best in the election.. This is the first
            equivalence class in :attr:`order_`. For example, in :class:`RuleScoreNum`, it is the candidates that are
            tied for the best score.
        """
        # N.B.: it is recommended to override this method when it is possible to make computation cheaper.
        return self.order_[0]

    @cached_property
    def winner_(self) -> object:
        """
        Winner of the election.

        :return: the winner of the election. This is the first candidate in :attr:`strict_order_` and also the
            choose of the tie-breaking rule in :attr:`cowinners_`.
        """
        return self.tie_break.choose(self.cowinners_)

    @cached_property
    def cotrailers_(self) -> NiceSet:
        """
        "Cotrailers" of the election.

        :return: the set of "cotrailers", i.e. the candidates that fare worst in the election. This is the last
            equivalence class in :attr:`order_`. For example, in :class:`RuleScoreNum`, it is the candidates that
            are tied for the worst score.
        """
        # N.B.: it is recommended to override this method when it is possible to make computation cheaper.
        return self.order_[-1]

    @cached_property
    def trailer_(self) -> object:
        """
        "Trailer" of the election.

        :return: the "trailer" of the election. This is the last candidate in :attr:`strict_order_` and also the
            unfavorable choose of the tie-breaking rule in :attr:`cotrailers_`.
        """
        if self.n_candidates_ == 1:
            return list(self.candidates_)[0]
        if len(self.cotrailers_) == self.n_candidates_:
            # Be careful not to output the winner (especially for random tie-breaking).
            return self.tie_break.choose(
                [candidate for candidate in self.cotrailers_ if candidate != self.winner_], reverse=True)
        return self.tie_break.choose(self.cotrailers_, reverse=True)

    @cached_property
    def order_(self) -> list:
        """
        Result of the election as a (weak) order over the candidates.

        :return: a list of :class:`NiceSet`. The first set contains the candidates that are tied for victory, etc.
        """
        raise NotImplementedError

    @cached_property
    def strict_order_(self) -> list:
        """
        Result of the election as a strict order over the candidates.

        :return: a list whose first element is the winner, etc. This may use the tie-breaking rule.
        """
        strict_order = [candidate for tie_class in self.order_ for candidate in self.tie_break.sort(tie_class)]
        # Check if this is consistent with ``self.winner_`` and ``self.trailer_`` (especially for random tie-breaking).
        if strict_order[0] != self.winner_:
            strict_order.remove(self.winner_)
            strict_order.insert(0, self.winner_)
        if strict_order[-1] != self.trailer_:
            strict_order.remove(self.trailer_)
            strict_order.append(self.trailer_)
        return strict_order

    # Methods to ensure compatibility with parent class RuleCommittee

    @cached_property
    def cowinning_committees_(self) -> NiceSet:
        return NiceSet({NiceFrozenSet({candidate}) for candidate in self.cowinners_})

    @cached_property
    def winning_committee_(self) -> NiceSet:
        return NiceSet({self.winner_})

    @cached_property
    def cotrailing_committees_(self) -> NiceSet:
        return NiceSet({NiceFrozenSet({candidate}) for candidate in self.cotrailers_})

    @cached_property
    def trailing_committee_(self) -> NiceSet:
        return NiceSet({self.trailer_})

    @cached_property
    def order_on_committees_(self) -> list:
        return [NiceSet({NiceFrozenSet({candidate}) for candidate in tie_class}) for tie_class in self.order_]

    @cached_property
    def strict_order_on_committees_(self) -> list:
        return [NiceSet({candidate}) for candidate in self.strict_order_]
