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
from whalrus.rules.rule_borda import RuleBorda
from whalrus.rules.rule_approval import RuleApproval
from whalrus.utils.utils import cached_property, my_division, NiceDict, DeleteCacheMixin, NiceSet
from whalrus.priorities.priority_budgeting import PriorityBudgeting
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union

import numpy as np

class ParticipatoryBudgeting(DeleteCacheMixin):

    """
    Participatory Budgeting tries to find to best set of candidates regarding the preferences
    of the voters, giving that there is a maximum amount to be spent and all candidate have 
    a cost strictly greater than 0

    Parameters
    ----------
    args 
        If present, these parameters will be passed to ``__call__`` immediately after initialization.
    base_rule : Rule
        Default : :class: 'RuleApproval'
        Define which rule is used to compute utilities. Generally it is a multiwinner rule, even if participatory
        budgeting aims at selecting several candidates
    tie_break : Priority
        Default : :class: 'ProrityBudgeting'
    converter : Converter
        Default : :class: 'ConverterBallotGeneral'
    budget : int
        Default : None 
        Define the limit amount that should not be exceeded, i.e the sum selected projects costs should be less 
        or equal than this amount.
    project_cost : dict
        Default : None
        Map the each project (= candidate) to his cost.
    kwargs 
        If present, these parameters will be passed to ``__call__`` immediately after initialization.

    Attributes 
    ----------
    profile_original_ : Profile
        The profile as it is entered by the user. Since it uses the constructor of :class:`Profile`, it indirectly uses
        :class:`ConverterBallotGeneral` to ensure, for example, that strings like ``'a > b > c'`` are converted to
        :class:`Ballot` objects.
    profile_converted_ : Profile
        The profile, with ballots that are adapted to the voting rule. For example, in :class:`RulePlurality`, it will
        be :class:`BallotPlurality` objects, even if the original ballots are :class:`BallotOrder` objects. This uses
        the parameter ``converter`` of the rule.
    candidates_ : NiceSet
        The candidates of the election, as entered in the ``__call__``.
        Could be explicitly specified by the user or deducted from the project_cost_ keys.
    budget_ : int
        Used in method when the object is called several times with a different budget.
        This allows to have a clear distinction between the actual budget and the initial one in parameters.
    project_cost_ : dict
        Used in method when the object is called several set of candidates.
        This allows to have a clear distinction between the actual set of candidates and the initial one in parameters.
    """

    def __init__(self,*args,base_rule : Rule = None, budget : int = None, #Might be better if budget and cost were not optional
                project_cost = None,converter = None,tie_break = PriorityBudgeting(), **kwargs):

        if base_rule is None:
            base_rule = RuleApproval()
        self.base_rule = base_rule
        self.tie_break= tie_break
        self.eliminated = []
        self.budget = budget 
        self.project_cost = project_cost
        if converter is None:
            converter = ConverterBallotGeneral()
        self.converter = converter
        self.profile_original_ = None
        self.profile_converted_ = None
        self.candidates_ = None
        if args or kwargs:
            self(*args, **kwargs)
        

    def __call__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, budget : int = None, project_cost : dict() = None):
        self.project_cost_ = self.project_cost
        if project_cost is not None:
            self.project_cost_ = project_cost
        if budget is not None:
            self.budget = budget
        if candidates is None:
            candidates = NiceSet(self.project_cost_.keys())
        if ballots is not None:
            self.profile_original_ = Profile(ballots, weights=weights, voters=voters)
            self.profile_converted_ = Profile([self.converter(b, candidates) for b in self.profile_original_],
                                          weights=self.profile_original_.weights, voters=self.profile_original_.voters)
        for i in range(len(self.profile_converted_._voters)):
            if self.profile_converted_._voters[i] is None:
                self.profile_converted_._voters[i] = i
        self.candidates_ = candidates
        self.voters_ = self.profile_converted_._voters
        self._check_profile(candidates)
        self.delete_cache()
        return self

    def _check_profile(self, candidates: set) -> None:
        if any([b.candidates != candidates for b in self.profile_converted_]):
            logging.warning('Some ballots do not have the same set of candidates as the whole election.')


    @cached_property
    def intial_voters_budget(self) -> NiceDict():
        """
        :returns: The initial budget repartition for each voter
        """
        voters_budget = {}
        for i, voter in enumerate(self.profile_converted_.voters):
            voters_budget[voter] = my_division(self.profile_converted_.weights[i]*self.budget, np.sum(self.profile_converted_.weights))
        return NiceDict(voters_budget)

    @cached_property
    def base_rule_(self):
        """
        :return: The rule that is used to compute the utilities
        """
        return self.base_rule(ballots = self.profile_original_, candidates = self.candidates_)

    @cached_property
    def initial_vote_counts(self) -> dict():
        """
        :returns:  The score for each project 
        """
        initial_vote_counts = {}
        for c in self.project_cost.keys():
            if self.base_rule_.gross_scores_[c] > 0:
                initial_vote_counts[c] = self.base_rule_.gross_scores_[c]
        return initial_vote_counts

    @cached_property
    def voters_utilities(self) -> dict():
        """
        :returns: The preferences for each voter
        """
        all_utilities = {}
        for ballot, weight, voter in self.base_rule_.profile_converted_.items():
            all_utilities[voter] = NiceDict({candidate: self.base_rule.scorer(ballot=ballot, candidates=self.candidates_).scores_[candidate]*weight
                    for candidate in ballot.candidates})

        return all_utilities
    
    @cached_property
    def supporters(self) -> dict():
        """
        :returns: Which set of voters voted for each project
        """
        return NiceDict({c : [voter for voter in self.voters_ 
                        if c in self.voters_utilities[voter] and self.voters_utilities[voter][c] > 0] for c in self.candidates_})
            

