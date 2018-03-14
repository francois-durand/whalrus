from whalrus.ballots.UtilityBallot import UtilityBallot
from whalrus.ballots.SingleCandidateBallot import SingleCandidateBallot



def make_plurality_ballot(b):
    if not isinstance(b, UtilityBallot):
        b = UtilityBallot(b)

    biggest_val = max(b.values())
    arg_maxs = [c for (c, v) in b.items() if v == biggest_val]

    if len(arg_maxs) > 1:
        raise Exception('Failed to convert ballot to plurality ballot because many candidates have the same score')

    return SingleCandidateBallot(first(arg_maxs), weight=b.weight)
