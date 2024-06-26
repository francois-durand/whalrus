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
from whalrus.priorities.priority import Priority,PriorityAscending
from operator import itemgetter
from typing import Union

project_cost = tuple[str, float]
project_cost_count = tuple[str, float, float]

class PriorityBudgeting():
    
    def __init__(self, name : str = None, count : bool = False, cost : bool = False, base_priority = None):
        self.name = name
        if base_priority is None:
            base_priority = PriorityAscending()
        self.base_priority = base_priority

    def _choose(self, x: list[project_cost]):
        raise NotImplementedError

class PriorityBudgetingAscendingCount(PriorityBudgeting):

    def __init__(self, cost = False, high = False, base_priority = None):
        self.cost = cost
        if high:
            self.next_priority = PriorityBudgetingAscendingCost()
        else:
            self.next_priority = PriorityBudgetingDescendingCost()
        super().__init__(name = 'AscendingCount', cost = cost, base_priority = base_priority)

    def _choose(self, x: Union[list[project_cost], list[project_cost_count]]):
        best_count = max(x, key = itemgetter(1))[1]
        remaining = [x_ for x_ in x if x_[1] == best_count]
        if not self.cost:
            remaining = [x_[0] for x_ in remaining]
        else:
            remaining = [self.next_priority._choose(remaining)]
        return self.base_priority.choice(remaining)


        

class PriorityBudgetingAscendingCost(PriorityBudgeting):
    
    def __init__(self, count = False, base_priority = None):
        self.count = count
        super().__init__(name = 'AscendingCost', count = count,  base_priority = base_priority)

    def _choose(self, x: list[project_cost_count]):
        best_cost = max(x, key = itemgetter(2))[2]
        remaining = [x_ for x_ in x if x_[2] == best_cost]
        if not self.count:
            remaining = [x_[0] for x_ in remaining]
        else:
            next_priority = PriorityBudgetingAscendingCount()
            remaining = [next_priority._choose(remaining)]
        return self.base_priority.choice(remaining)

class PriorityBudgetingDescendingCost(PriorityBudgeting):
    
    def __init__(self, count = False, base_priority = None) :
        self.count = count
        super().__init__(name = 'DescendingCost', count = count, base_priority = base_priority)

    def _choose(self, x: list[project_cost_count]):
        best_cost = min(x, key = itemgetter(2))[2]
        remaining = [x_ for x_ in x if x_[2] == best_cost]
        if not self.count:
            remaining = [x_[0] for x_ in remaining]
        else:
            next_priority = PriorityBudgetingAscendingCount()
            remaining = [next_priority._choose(remaining)]
        return self.base_priority.choice(remaining)