from whalrus.profiles.profile import Profile
from whalrus.ballots.ballot_levels import BallotLevels

w_a1 = [24,21,24,23,22,25]

p_a1 = Profile([{'a':1, 'b':0,'c':1,'d':0},{'a':1, 'b':0,'c':1,'d':0},

        {'a':0, 'b':1,'c':0,'d':1}, {'a':0, 'b':1,'c':0,'d':0},
        {'a':0, 'b':1,'c':1,'d':1}, {'a':1, 'b':0,'c':0}], weights = w_a1)

candidates = ['a','b','c','d']

p_a2 = Profile(ballots=[
    BallotLevels({'a':1, 'b':0,'c':1,'d':0}, candidates = candidates),
    BallotLevels({'a':1, 'b':0,'c':1,'d':0}, candidates = candidates),
    BallotLevels({'a':0, 'b':1,'c':0,'d':1}, candidates = candidates),
    BallotLevels({'a':0, 'b':1,'c':0,'d':0}, candidates = candidates),
    BallotLevels({'a':0, 'b':1,'c':1,'d':1}, candidates = candidates),
    BallotLevels({'a':1, 'b':0,'c':0}, candidates = candidates)])