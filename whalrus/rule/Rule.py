import logging
from whalrus.utils.Utils import DeleteCacheMixin, cached_property, NiceSet
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class Rule(DeleteCacheMixin):
    """
    A voting rule.

    :param ballots: if mentioned, will be passed to `__call__` immediately after initialization.
    :param weights: if mentioned, will be passed to `__call__` immediately after initialization.
    :param voters: if mentioned, will be passed to `__call__` immediately after initialization.
    :param candidates: if mentioned, will be passed to `__call__` immediately after initialization.
    :param converter: if mentioned, will be passed to `__call__` immediately after initialization.
    :param tie_break: a tie-break rule.
    :param default_converter: the default converter that is used to convert input ballots. This converter is
        used when no converter is explicitly given to `__call__`. Default: :class:`ConverterBallotGeneral`.

    A :class:`Rule` object is a callable whose inputs are ballots and optionally weights, voters, candidates and a
    converter. When the rule is called, it loads the profile. The output of the call is the rule itself. But
    after the call, you can access to the computed variables (ending with an underscore), such as
    :attr:`cowinners_`.

    At the initialization of a :class:`Rule` object, some options can be given, such as a tie-break rule and a
    default converter. In some subclasses, there can also be an option about the way to count abstentions, etc.

    Cf. :class:`RulePlurality` for some examples.
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, default_converter: ConverterBallot = None):
        """
        Remark: this `__init__` must always be called at the end of the subclasses' `__init__`.
        """
        if default_converter is None:
            default_converter = ConverterBallotGeneral()
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

    def __call__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None):
        self.profile_ = Profile(ballots, weights=weights, voters=voters)
        if converter is None:
            converter = self.default_converter
        self.profile_converted_ = Profile([converter(b, candidates) for b in self.profile_],
                                          weights=self.profile_.weights, voters=self.profile_.voters)
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
    def cowinners_(self) -> NiceSet:
        """
        Cowinners of the election.

        :return: the set of cowinners.
        """
        return self.order_[0]

    @cached_property
    def winner_(self) -> object:
        """
        Winner of the election.

        :return: the winner of the election (which may use a tie-breaking rule).
        """
        return self.tie_break.choice(self.cowinners_)

    @cached_property
    def cotrailers_(self) -> NiceSet:
        """
        "Cotrailers" of the election.

        The candidates that fare worst in the election. For example, in a rule based on a notion of score, it would
        be the candidates that are tied for worst score.

        :return: the set of "cotrailers".
        """
        return self.order_[-1]

    @cached_property
    def trailer_(self) -> object:
        """
        "Trailer" of the election.

        :return: the "trailer" of the election (which may use a tie-breaking rule).
        """
        return self.tie_break.choice(self.cotrailers_, reverse=True)

    @cached_property
    def order_(self) -> list:
        """
        Result of the election as a (weak) order over the candidates.

        :return: a list of sets (or, more exactly, :class:`NiceSet` objects). The first set contains the candidates
            that are tied for victory, etc.
        """
        raise NotImplementedError

    @cached_property
    def strict_order_(self) -> list:
        """
        Result of the election as a strict order over the candidates.

        :return: a list whose first element is the winner, etc (which may use a tie-breaking rule).
        """
        return [candidate for tie_class in self.order_ for candidate in self.tie_break.sort(tie_class)]
