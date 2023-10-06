from whalrus.utils.preflib_io import profile_from_preflib
from whalrus.ballots.ballot_order import BallotOrder
import pytest

def test_profile_preflib_toi():
    file ="""
# FILE NAME: foo.toi
# TITLE: Foo Election
# DESCRIPTION: Some Description
# DATA TYPE: toi
# ALTERNATIVE NAME 1: Anna
# ALTERNATIVE NAME 2: Belle
# ALTERNATIVE NAME 3: Chris
# ALTERNATIVE NAME 4: Dave
1: 3,1,2
3: 3,{1,2},4
2: {1,2},3,4
1: 4,{3,2,1}
"""
    assert profile_from_preflib(raw_data=file) == [
        BallotOrder([3,1,2], candidates={1,2,3,4}),
        BallotOrder([3,{1,2},4], candidates={1,2,3,4}),
        BallotOrder([3,{1,2},4], candidates={1,2,3,4}),
        BallotOrder([3,{1,2},4], candidates={1,2,3,4}),
        BallotOrder([{1,2},3,4], candidates={1,2,3,4}),
        BallotOrder([{1,2},3,4], candidates={1,2,3,4}),
        BallotOrder([4,{1,2,3}], candidates={1,2,3,4})
        ]

def test_profile_preflib_soi():
    file ="""
# FILE NAME: foo.soi
# TITLE: Foo Election
# DESCRIPTION: Some Description
# DATA TYPE: soi
# ALTERNATIVE NAME 1: Anna
# ALTERNATIVE NAME 2: Belle
# ALTERNATIVE NAME 3: Chris
# ALTERNATIVE NAME 4: Dave
1: 3,1,2
2: 3,4
1: 1,2,4
1: 4,3,2
"""
    assert profile_from_preflib(raw_data=file) == [
        BallotOrder([3,1,2], candidates={1,2,3,4}),
        BallotOrder([3,4], candidates={1,2,3,4}),
        BallotOrder([3,4], candidates={1,2,3,4}),
        BallotOrder([1,2,4], candidates={1,2,3,4}),
        BallotOrder([4,3,2], candidates={1,2,3,4}),
        ]

def test_profile_preflib_unsupported():
    file ="""
# FILE NAME: foo.cat
# TITLE: Foo Election
# DESCRIPTION: Some Description
# DATA TYPE: cat
# CATEGORY NAME 1: Yes
# CATEGORY NAME 2: No
# ALTERNATIVE NAME 1: Anna
# ALTERNATIVE NAME 2: Belle
# ALTERNATIVE NAME 3: Chris
# ALTERNATIVE NAME 4: Dave
1: {3,1},2
2: 3,4
1: {1,2},4
1: {4,3},2
"""
    with pytest.raises(ValueError):
        profile_from_preflib(raw_data=file)