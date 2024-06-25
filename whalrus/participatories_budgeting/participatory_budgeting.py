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
import logging
from whalrus.rules_committee.rule_committee import RuleCommittee
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.rules.rule import Rule
from whalrus.participatories_budgeting.voters_wallet import VotersWallet
from whalrus.rules.rule_borda import RuleBorda
from whalrus.utils.utils import cached_property, my_division, NiceDict, DeleteCacheMixin, NiceSet
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union

import numpy as np

class ParticipatoryBudgeting(DeleteCacheMixin):

    def __init__(self,*args,base_rule : Rule, project_cost : dict(), budget : int, converter = None, **kwargs):

        self.base_rule = base_rule
        self.project_cost = project_cost
        self.budget = budget
        if converter is None:
            converter = ConverterBallotGeneral()
        self.converter = converter
        # Computed variables
        self.profile_original_ = None
        self.profile_converted_ = None
        self.candidates_ = None
        # Optional: load a profile at initialization
        if args or kwargs:
            self(*args, **kwargs)
        

    def __call__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None):
        self.profile_original_ = Profile(ballots, weights=weights, voters=voters)
        self.profile_converted_ = Profile([self.converter(b, candidates) for b in self.profile_original_],
                                          weights=self.profile_original_.weights, voters=self.profile_original_.voters)
        for i in range(len(self.profile_converted_._voters)):
            if self.profile_converted_._voters[i] is None:
                self.profile_converted_._voters[i] = i
        if candidates is None:
            candidates = NiceSet(set().union(*[b.candidates for b in self.profile_converted_]))
        self.candidates_ = candidates
        self.voters_ = self.profile_converted_._voters
        self._check_profile(candidates)
        self.delete_cache()
        return self

    def _check_profile(self, candidates: set) -> None:
        if any([b.candidates != candidates for b in self.profile_converted_]):
            logging.warning('Some ballots do not have the same set of candidates as the whole election.')


    @cached_property
    def intial_voters_budget(self):
        voters_budget = {}
        for i, voter in enumerate(self.profile_converted_.voters):
            voters_budget[voter] = my_division(self.profile_converted_.weights[i]*self.budget, np.sum(self.profile_converted_.weights))
        return NiceDict(voters_budget)

    @cached_property
    def base_rule_(self):
        return self.base_rule(ballots = self.profile_converted_, candidates = self.candidates_)

    @cached_property
    def initial_vote_counts(self):
        initial_vote_counts = {}
        for c in self.project_cost.keys():
            if self.base_rule_.gross_scores_[c] > 0:
                initial_vote_counts[c] = self.base_rule_.gross_scores_[c]
        return initial_vote_counts

    @cached_property
    def voters_utilities(self):
        all_utilities = {}
        for ballot, weight, voter in self.profile_converted_.items():
            all_utilities[voter] = NiceDict({candidate: self.base_rule.scorer(ballot=ballot, candidates=self.candidates_).scores_[candidate]*weight
                    for candidate in self.candidates_})

        return all_utilities
    
    @cached_property
    def supporters(self):
        return NiceDict({c : [voter for voter in self.voters_ 
                        if self.voters_utilities[voter][c] > 0] for c in self.candidates_})
            

