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
from whalrus.rule.Rule import Rule
from whalrus.priority.Priority import Priority
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class RuleMultiWinner(Rule):
    """
    A Multiwinner (committee) voting rule.

    :param ballots: if mentioned, will be passed to ``__call__`` immediately after initialization.
    :param weights: if mentioned, will be passed to ``__call__`` immediately after initialization.
    :param voters: if mentioned, will be passed to ``__call__`` immediately after initialization.
    :param candidates: if mentioned, will be passed to ``__call__`` immediately after initialization.
    :param committee_size: if mentioned, will be passed to ``__call__`` immediately after initialization.
    :param tie_break: a multiwinner tie-break rule.
    :param converter: the converter that is used to convert input ballots in order to compute
        :attr:`profile_converted_`. Default: :class:`ConverterBallotGeneral`.

    A :class:`Rule` object is a callable whose inputs are ballots and optionally weights, voters and candidates.
    When the rule is called, it loads the profile. The output of the call is the rule itself. But
    after the call, you can access to the computed variables (ending with an underscore), such as
    :attr:`cowinners_`.

    At the initialization of a :class:`Rule` object, some options can be given, such as a tie-break rule. In some
    subclasses, there can also be an option about the way to count abstentions, etc.

    Cf. :class:`RuleMultiWinnerBloc` for some examples.

    :ivar profile_original\_: the profile as it is entered by the user. Since it uses the constructor of
        :class:`Profile`, it indirectly uses :class:`ConverterBallotGeneral` to ensure, for example, that strings like
        ``'a > b > c'`` are converted to :class:`Ballot` objects.
    :ivar profile_converted\_: the profile, with ballots that are adapted to the voting rule. For example,
        in :class:`RulePlurality`, it will be :class:`BallotPlurality` objects, even if the original ballots are
        :class:`BallotOrder` objects. This uses the parameter ``converter`` of the rule.
    :ivar candidates\_: the candidates of the election, as entered in the ``__call__``.
    """

    def __init__(self, ballots: Union[list, Profile] = None,
                 weights: list = None, voters: list = None,
                 candidates: set = None, committee_size: int = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS,
                 converter: ConverterBallot = None):
        self.committee_size = committee_size
        super().__init__(
            ballots=ballots, weights=weights, voters=voters,
            candidates=candidates,
            tie_break=tie_break, converter=converter
        )
