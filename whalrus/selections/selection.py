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
from whalrus.utils.utils import my_division, NiceDict
from whalrus.profiles.profile import Profile
from whalrus.rules.rule_plurality import RulePlurality

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
    def get_winner_ratio_(self):
        return NiceDict({candidate:my_division(self.rule_.gross_scores_[candidate] - self.threshold, 
                    self.rule_.gross_scores_[candidate]) for candidate in self.selected_})

    @cached_property
    def new_profile_(self):
        

        if len(self.selected_) != 0:
            ballots, weights = [], []
            new_set = self.remaining_
            new_set_ = self.rule_.candidates_
 
            for ballot, weight, _ in self.rule_.profile_original_.items():
              
                ballot = ballot.restrict(new_set_)
                
                if len(ballot) >= 1 and ballot.first() not in self.selected_:
                    ballots.append(ballot.restrict(new_set))
                    weights.append(weight)
                
                elif len(ballot) > 1 and self.get_winner_ratio_[ballot.first()] > 0:
                    
                    ballots.append(ballot.restrict(new_set))
                    weights.append(weight*self.get_winner_ratio_[ballot.first()])
            
            return Profile(ballots, weights = weights)

        return self.rule_.profile_original_

    @cached_property
    def selected_order_(self) -> list:
        """list: The order on the selected candidates.

        It is a list where each element is a :class:`NiceSet`. Each set represents a class of tied candidates. The
        first set in the list represents the "best" eliminated candidates, whereas the last set represent the "worst"
        candidates.
        """
        raise  

    @cached_property
    def selected_(self) -> NiceSet:
        """NiceSet: The selected candidates.
        """
        return NiceSet(c for tie_class in self.selected_order_ for c in tie_class)

    @cached_property
    def remaining_(self) -> NiceSet:
        """NiceSet: The candidates that remain after selection.
        """
        return NiceSet(self.rule_.candidates_ - self.selected_)

