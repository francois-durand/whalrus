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
from whalrus.utils.utils import DeleteCacheMixin, cached_property, NiceSet, NiceFrozenSet
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union
from itertools import combinations

class RuleTransfert(DeleteCacheMixin):
    """
    A multi-winner rule that selects the best candidates using transfert of ballots
    """

    def __init__(self, *args, tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None, **kwargs):
        """
        Remark: this `__init__` must always be called at the end of the subclasses' `__init__`.
        """
        if converter is None:
            converter = ConverterBallotGeneral()
        # Parameters
        self.tie_break = tie_break
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
        if candidates is None:
            candidates = NiceSet(set().union(*[b.candidates for b in self.profile_converted_]))
        self.candidates_ = candidates
        self._check_profile(candidates)
        self.delete_cache()
        return self

    def _check_profile(self, candidates: set) -> None:
        if any([b.candidates != candidates for b in self.profile_converted_]):
            logging.warning('Some ballots do not have the same set of candidates as the whole election.')

    @cached_property
    def n_candidates_(self) -> int:
        """
        Number of candidates.

        :return: the number of candidates.
        """
        return len(self.candidates_)

    @cached_property
    def rounds_position_(self):
        """Use score to convert to candidates position at each rounds"""
        rounds_position = []
        for i, round in enumerate(self.get_rounds_):
            elected_position = {}
         
            for j, c in enumerate(round[1]):
                elected_position[c] = len(self.candidates_) - j
            eliminated_position = {}
            for j, c in enumerate(round[3]):
                eliminated_position[c] = j + 1
            order = round[0].rule_.strict_order_
            remaining_position = {}
            for j, c in enumerate(reversed(order)):
                if len(round[2]) > 0:
                    remaining_position[c] = j + 1 + len(round[3])

            rounds_position.append((elected_position, remaining_position, eliminated_position))
        return rounds_position


    @cached_property
    def get_rounds_(self) -> list:
        raise NotImplementedError

    @cached_property
    def winning_committee_(self) -> NiceSet:
        """
        Select the k best elected by the designed method.
        """
        return NiceFrozenSet(list(self.scores_last_rounds[0].keys())[:self.committee_size])
    
    @cached_property
    def order_on_committees_(self) -> list:
        """
        Construct a list of two set including the winning committee on left 
        and all others possibilities on right. 
        """
        return [NiceSet({self.winning_committee_}), NiceSet(NiceFrozenSet(set(i)) 
                for i in combinations(self.candidates_, self.committee_size) if set(i) not in NiceSet({self.winning_committee_}))]

    @cached_property
    def strict_order_on_committees_(self) -> list:
        """
        Construct a list with the winning committee as first
        and followed by all others possibilities.  
        """
        L = [NiceFrozenSet(i)
                for i in combinations(self.candidates_, self.committee_size) if set(i) not in NiceSet({self.winning_committee_})]
        return [self.winning_committee_] + L


    @cached_property 
    def eliminated_committee_(self) -> set:
        """
        Return the whole set of the eliminated candidates.
        """
        return NiceFrozenSet(self.scores_last_rounds[2].keys())

    @cached_property
    def scores_rounds_(self) -> list:
        """
        Give the scores of both selected and eliminated candidates at each round.
        """
        return [(scores_elected, scores_remaining,scores_eliminated) for _,scores_elected,scores_remaining ,scores_eliminated in self.get_rounds_]

    @cached_property
    def scores_last_rounds(self):
        """
        Give the scores of both selected and eliminated candidates at the last round.
        """
        return self.scores_rounds_[-1]

    @cached_property
    def get_transfert(self):

        d = dict()
        for rounds in self.get_rounds_:
            d.update(rounds[0].transfert_)
        return d