import logging
from whalrus.utils.Utils import DeleteCacheMixin, cached_property
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class Rule(DeleteCacheMixin):

    def __init__(self, ballots: Union[list, Profile]=None, weights: list=None, voters: list=None,
                 candidates: set=None, converter: ConverterBallot=None,
                 tie_break: Priority=Priority.UNAMBIGUOUS, default_converter: ConverterBallot=ConverterBallotGeneral()):
        """
        A voting rule.

        :param ballots: if mentioned, will be passed to `__call__` immediately after initialization.
        :param weights: if mentioned, will be passed to `__call__` immediately after initialization.
        :param voters: if mentioned, will be passed to `__call__` immediately after initialization.
        :param candidates: if mentioned, will be passed to `__call__` immediately after initialization.
        :param converter: if mentioned, will be passed to `__call__` immediately after initialization.
        :param tie_break: a tie-break rule.
        :param default_converter: the default converter that is used to convert input ballots. This converter is
            used when no converter is explicitly given to `__call__`.

        A :class:`Rule` object is a callable whose inputs are ballots and optionally weights, voters, candidates and a
        converter. When the rule is called, it loads the profile. The output of the call is the rule itself. But
        after the call, you can access to the computed variables (ending with an underscore), such as
        :attr:`cowinners_`.

        At the initialization of a :class:`Rule` object, some options can be given, such as a tie-break rule and a
        default converter. In some subclasses, there can also be an option about the way to count abstentions, etc.

        Cf. :class:`RulePlurality` for some examples.

        Remark: this `__init__` must always be called at the end of the subclasses' `__init__`.
        """
        # Parameters
        self.tie_break = tie_break
        self.default_converter = default_converter
        # Computed variables
        self.profile_ = None
        self.profile_converted_ = None
        self.candidates_ = None
        # Optional: load a profile at initialization
        if ballots is not None:
            self(ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter)

    def __call__(self, ballots: Union[list, Profile]=None, weights: list=None, voters: list=None,
                 candidates: set=None, converter: ConverterBallot=None) -> 'Rule':
        self.profile_ = Profile(ballots, weights=weights, voters=voters)
        if converter is None:
            converter = self.default_converter
        self.profile_converted_ = Profile([converter(b, candidates) for b in self.profile_],
                                          weights=weights, voters=voters)
        if candidates is None:
            candidates = set().union(*[b.candidates for b in self.profile_converted_])
        self.candidates_ = candidates
        self._check_profile(candidates)
        self.delete_cache()
        return self

    def _check_profile(self, candidates: set) -> None:
        if any([b.candidates != candidates for b in self.profile_converted_]):
            logging.warning('Some ballots do not have the same set of candidates as the whole election.')

    @cached_property
    def cowinners_(self) -> set:
        """
        Cowinners of the election.

        :return: the set of ex-aequo winners.
        """
        raise NotImplementedError

    @cached_property
    def winner_(self) -> object:
        """
        Winner of the election.

        :return: the winner of the election (which may use a tie-breaking rule).
        """
        return self.tie_break.choice(self.cowinners_)
