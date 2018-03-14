from whalrus.ballots.UtilityBallot import UtilityBallot
from toolz import first

class SingleCandidateBallot(UtilityBallot):

    def candidate(self):
        return first(self.keys())


