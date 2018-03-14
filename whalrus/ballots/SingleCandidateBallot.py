from whalrus.ballots.UtilityBallot import UtilityBallot

class SingleCandidateBallot(UtilityBallot):

    def to_plurality_ballot(self):
        min(self.values())


