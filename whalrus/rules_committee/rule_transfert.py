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
from whalrus.utils.utils import DeleteCacheMixin, cached_property, NiceSet
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot_general import ConverterBallotGeneral
from whalrus.profiles.profile import Profile
from whalrus.converters_ballot.converter_ballot import ConverterBallot
from typing import Union


class RuleTransfert(DeleteCacheMixin):
    """
    A voting rule, a priori designed to elect a committee (set of candidates).

    :param `*args`: if present, these parameters will be passed to ``__call__`` immediately after initialization.
    :param tie_break: a tie-break rule.
    :param converter: the converter that is used to convert input ballots in order to compute
        :attr:`profile_converted_`. Default: :class:`ConverterBallotGeneral`.
    :param `**kwargs`: if present, these parameters will be passed to ``__call__`` immediately after initialization.

    A :class:`RuleCommittee` object is a callable whose inputs are ballots and optionally weights, voters and
    candidates. When the rule is called, it loads the profile. The output of the call is the rule itself. But
    after the call, you can access to the computed variables (ending with an underscore), such as
    :attr:`cowinning_committees_`.

    At the initialization of a :class:`RuleCommittee` object, some options can be given, such as a tie-break rule or a
    converter. In some subclasses, there can also be an option about the way to count abstentions, etc.

    Cf. :class:`RulePlurality` for some examples.

    :ivar profile_original\_: the profile as it is entered by the user. Since it uses the constructor of
        :class:`Profile`, it indirectly uses :class:`ConverterBallotGeneral` to ensure, for example, that strings like
        ``'a > b > c'`` are converted to :class:`Ballot` objects.
    :ivar profile_converted\_: the profile, with ballots that are adapted to the voting rule. For example,
        in :class:`RulePlurality`, it will be :class:`BallotPlurality` objects, even if the original ballots are
        :class:`BallotOrder` objects. This uses the parameter ``converter`` of the rule.
    :ivar candidates\_: the candidates of the election, as entered in the ``__call__``.
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
    def get_rounds_(self) -> list:
        raise NotImplementedError

    @cached_property
    def winning_committee_(self) -> NiceSet:
        
        return NiceSet(self.scores_last_rounds[0].keys())
    

    @cached_property 
    def eliminated_committee_(self) -> NiceSet:
        """
        Return the whole set of the eliminated candidates
        """
        return NiceSet(self.scores_last_rounds[1].keys())

    @cached_property
    def scores_rounds_(self) -> list:
        return [(scores_elected, scores_eliminated) for _,scores_elected, scores_eliminated in self.get_rounds_[1:]]

    @cached_property
    def scores_last_rounds(self):
        return self.scores_rounds_[-1]
