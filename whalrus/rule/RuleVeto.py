import logging
from whalrus.rule.RuleScore import RuleScore
from whalrus.priority.Priority import Priority
from whalrus.converter_ballot.ConverterBallotToVeto import ConverterBallotToVeto
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.profile.Profile import Profile
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from typing import Union


class RuleVeto(RuleScore):
    """
    The veto rule.

    :param default_converter: the default is :class:`ConverterBallotToVeto`.

    >>> RuleVeto(['a', 'b', 'b', 'c', 'c']).winner_
    'a'
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None, converter: ConverterBallot = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, default_converter: ConverterBallot = None):
        if default_converter is None:
            default_converter = ConverterBallotToVeto()
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
            scores_[ballot.candidate] -= weight
        return scores_
