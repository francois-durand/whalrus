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


class RuleCommittee(DeleteCacheMixin):
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
    def cowinning_committees_(self) -> NiceSet:
        """
        Cowinning committees.

        :return: the set of cowinning committees, i.e. the committees (sets of candidates) that fare best in the
            election. This is the first equivalence class in :attr:`order_on_committees_`. For example, if any
            legal committee is assigned a numeric score, it is the committees that are tied for the best score.
        """
        # N.B.: it is recommended to override this method when it is possible to make computation cheaper.
        return self.order_on_committees_[0]

    @cached_property
    def winning_committee_(self) -> NiceSet:
        """
        Winning committee.

        :return: the winning committee of the election. This is the first committee in
            :attr:`strict_order_on_committees_` and also the choice of the tie-breaking rule in
            :attr:`cowinning_committees_`.
        """
        # noinspection PyTypeChecker
        return self.tie_break.choose_committee(self.cowinning_committees_)

    @cached_property
    def cotrailing_committees_(self) -> NiceSet:
        """
        "Cotrailing" committees.

        :return: the set of "cotrailing" committees, i.e. the committees (sets of candidates) that fare worst in the
            election. This is the last equivalence class in :attr:`order_on_committees_`. For example, if any
            legal committee is assigned a numeric score, it is the committees that are tied for the worst score.
        """
        # N.B.: it is recommended to override this method when it is possible to make computation cheaper.
        return self.order_on_committees_[-1]

    @cached_property
    def trailing_committee_(self) -> NiceSet:
        """
        "Trailing" committee of the election.

        :return: the "trailing" committee of the election. This is the last committee in
            :attr:`strict_order_on_committees` and also the unfavorable choice of the tie-breaking rule in
            :attr:`cotrailing_committees_`.
        """
        if len(self.cotrailing_committees_) == 1:
            return list(self.cotrailing_committees_)[0]
        if self.winning_committee_ in self.cotrailing_committees_:
            # Be careful not to output the winner (especially for random tie-breaking).
            # noinspection PyTypeChecker
            return self.tie_break.choose_committee(
                [committee for committee in self.cotrailing_committees_ if committee != self.winning_committee_],
                reverse=True)
        # noinspection PyTypeChecker
        return self.tie_break.choose_committee(self.cotrailing_committees_, reverse=True)

    @cached_property
    def order_on_committees_(self) -> list:
        """
        Result of the election as a (weak) order over the legal committees.

        :return: a list of :class:`NiceSet`. The first set contains the committees that are tied for victory, etc.
        """
        raise NotImplementedError

    @cached_property
    def strict_order_on_committees_(self) -> list:
        """
        Result of the election as a strict order over the legal committees.

        :return: a list whose first element is the winning committee, etc. This may use the tie-breaking rule.
        """
        strict_order = [committee
                        for tie_class in self.order_on_committees_
                        for committee in self.tie_break.sort_committees(tie_class)]
        # Check if this is consistent with ``self.winning_committee_`` and ``self.trailing_committee_``
        # (especially for random tie-breaking).
        if strict_order[0] != self.winning_committee_:
            strict_order.remove(self.winning_committee_)
            strict_order.insert(0, self.winning_committee_)
        if strict_order[-1] != self.trailing_committee_:
            strict_order.remove(self.trailing_committee_)
            strict_order.append(self.trailing_committee_)
        return strict_order
