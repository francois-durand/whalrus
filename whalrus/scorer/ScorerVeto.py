from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.scale.Scale import Scale
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.scorer.Scorer import Scorer


class ScorerVeto(Scorer):
    """
    A Veto scorer for :class:`BallotVeto`.
    """

    def __init__(self, ballot: BallotOrder = None, voter: object = None, candidates: set = None,
                 scale: Scale = None,
                 count_abstention: bool = False):
        self.count_abstention = count_abstention
        super().__init__(ballot=ballot, voter=voter, candidates=candidates, scale=scale)

    @cached_property
    def scores_(self) -> NiceDict:
        if self.ballot_.candidate is None:
            if self.count_abstention:
                return NiceDict({c: 0 for c in self.candidates_})
            else:
                return NiceDict()
        scores = NiceDict({c: 0 for c in self.candidates_})
        scores[self.ballot_.candidate] = -1
        return scores
