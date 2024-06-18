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

from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.profiles.profile import Profile
from whalrus.rules.rule import Rule

class ParticipatoryBudgeting(RuleCommittee):

    def __init__(self, profile : Profile, base_rule : Rule, project_cost : dict(), budget : int):

        self.profile = profile
        self.base_rule = base_rule
        self.project_cost = project_cost
        self.budget = budget

    @cached_property
    def get_voters_budget(self):
        pass
        