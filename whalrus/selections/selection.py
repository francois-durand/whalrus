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
from whalrus.utils.utils import cached_property, DeleteCacheMixin, NiceSet
from whalrus.rules.rule import Rule


class Selection(DeleteCacheMixin):
  

    def __init__(self, *args, **kwargs):
        """
        Remark: this `__init__` must always be called at the end of the subclasses' `__init__`.
        """
        # Computed variables
        self.rule_ = None
        # Optional: load a rule at initialization
        if args or kwargs:
            self(*args, **kwargs)

    def __call__(self, rule: Rule):
        self.rule_ = rule
        self.delete_cache()
        return self

    @cached_property
    def selected_order_(self) -> list:
        """list: The order on the selected candidates.

        It is a list where each element is a :class:`NiceSet`. Each set represents a class of tied candidates. The
        first set in the list represents the "best" eliminated candidates, whereas the last set represent the "worst"
        candidates.
        """
        raise NotImplementedError

    @cached_property
    def selected_(self) -> NiceSet:
        """NiceSet: The selected candidates.

        This should always be non-empty. It may contain all the candidates (for example, it is always the case
        when there was only one candidate in the election).
        """
        return NiceSet(c for tie_class in self.selected_order_ for c in tie_class)

    @cached_property
    def remaining_(self) -> NiceSet:
        """NiceSet: The candidates that remain after selection.
        """
        return NiceSet(self.rule_.candidates_ - self.selected_)
