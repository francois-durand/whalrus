import logging
from whalrus.rule.RuleScore import RuleScore
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallotToPlurality import ConverterBallotToPlurality
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class RulePlurality(RuleScore):
    """
    The plurality rule.

    In the most general syntax, firstly, you define the rule:

    >>> plurality = RulePlurality(tie_break=Priority.ASCENDING)

    Secondly, you use it as a callable to load a particular election (profile, candidates):

    >>> plurality(ballots=['a', 'b', 'c'], weights=[2, 2, 1], voters=['Alice', 'Bob', 'Cat'],
    ...           candidates={'a', 'b', 'c', 'd'})  # doctest:+ELLIPSIS
    <whalrus.rule.RulePlurality.RulePlurality object at ...>

    Finally, you can access the computed variables:

    >>> plurality.scores_
    {'a': 2, 'b': 2, 'c': 1, 'd': 0}
    >>> plurality.winner_
    'a'

    Later, if you wish, you can load another profile with the same voting rule, and so on.

    Optionally, you can specify an election (profile and candidates) as soon as the :class:`Rule` object is initialized.
    This allows for one-liners such as:

    >>> RulePlurality(['a', 'a', 'b', 'c']).winner_
    'a'

    Cf. :class:`Rule` for more information about the arguments.
    """

    def __init__(self, ballots: Union[list, Profile]=None, weights: list=None, voters: list=None,
                 candidates: set=None, converter: ConverterBallot=None,
                 tie_break: Priority=Priority.UNAMBIGUOUS,
                 default_converter: ConverterBallot=ConverterBallotToPlurality()):
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates, converter=converter,
            tie_break=tie_break, default_converter=default_converter
        )

    def _check_profile(self, candidates: set) -> None:
        if any([len(b.candidates) > 1 and b.candidates != candidates for b in self.profile_converted_]):
            logging.warning('Some ballots do not have the same set of candidates as the whole election.')

    @cached_property
    def scores_(self) -> NiceDict:
        scores_ = NiceDict({c: 0 for c in self.candidates_})
        for ballot, weight, _ in self.profile_converted_.items():
            if ballot.candidate is None:
                continue
            scores_[ballot.candidate] += weight
        return scores_
