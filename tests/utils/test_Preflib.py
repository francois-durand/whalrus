from whalrus.utils.preflib_io import profile_from_preflib
from whalrus.ballots.ballot_order import BallotOrder


def test_profile_preflib():
    file ="""
1: 3,1,2,4
2: 3,{1,2},4
3: {1,2},3,4
4: 4,{3,2,1}
"""
    assert profile_from_preflib(file) == [
        BallotOrder([3,1,2,4]),
        BallotOrder([3,{1,2},4]),
        BallotOrder([{1,2},3,4]),
        BallotOrder([4,{1,2,3}])
        ]