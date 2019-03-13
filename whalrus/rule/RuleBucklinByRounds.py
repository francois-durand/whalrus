from whalrus.scorer.ScorerBucklin import ScorerBucklin
from whalrus.rule.RuleScoreNum import RuleScoreNum
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.priority.Priority import Priority
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.profile.Profile import Profile
from typing import Union


class RuleBucklinByRounds(RuleScoreNum):
    """
    Bucklin's rule (round by round version).

    :param converter: the default is :class:`ConverterBallotToOrder`.
    :param scorer: the default is :class:`ScorerBucklin`.

    >>> rule = RuleBucklinByRounds(ballots=['a > b > c > d', 'b > a > c > d', 'c > a > b > d', 'd > a > b > c'])
    >>> rule.detailed_scores_
    [{'a': 0.25, 'b': 0.25, 'c': 0.25, 'd': 0.25}, {'a': 1.0, 'b': 0.5, 'c': 0.25, 'd': 0.25}]
    >>> rule.final_round_
    2
    >>> rule.scores_
    {'a': 1.0, 'b': 0.5, 'c': 0.25, 'd': 0.25}
    >>> rule.winner_
    'a'

    During the first round, a candidate's score is the proportion of voters who rank it first. During the second
    round, its score is the proportion of voters who rank it first or second. Etc. More precisely, at each round, the
    scorer is used with ``k`` equal to the round number; cf. :class:`ScorerBucklin`.

    Cf. also :class:`RuleBucklinInstant`.
    """

    def __init__(self, ballots: Union[list, Profile] = None, weights: list = None, voters: list = None,
                 candidates: set = None,
                 tie_break: Priority = Priority.UNAMBIGUOUS, converter: ConverterBallot = None,
                 scorer: ScorerBucklin = None):
        # Default value
        if converter is None:
            converter = ConverterBallotToOrder()
        if scorer is None:
            scorer = ScorerBucklin()
        # Parameters
        self.scorer = scorer
        super().__init__(
            ballots=ballots, weights=weights, voters=voters, candidates=candidates,
            tie_break=tie_break, converter=converter
        )

    @cached_property
    def detailed_scores_(self) -> list:
        n_candidates = len(self.candidates_)
        detailed_scores = []
        for k in range(1, n_candidates + 1):
            self.scorer.k = k
            brute_scores = NiceDict({c: 0. for c in self.candidates_})
            weights = NiceDict({c: 0 for c in self.candidates_})
            for ballot, weight, voter in self.profile_converted_.items():
                for c, value in self.scorer(ballot=ballot, voter=voter, candidates=self.candidates_).scores_.items():
                    brute_scores[c] += weight * value
                    weights[c] += weight
            scores = NiceDict({c: score / weights[c] if weights[c] > 0 else 0.
                               for c, score in brute_scores.items()})
            detailed_scores.append(scores)
            if max(scores.values()) > 0.5:
                break
        return detailed_scores

    @cached_property
    def scores_(self) -> NiceDict:
        return self.detailed_scores_[-1]

    @cached_property
    def final_round_(self) -> int:
        return len(self.detailed_scores_)
