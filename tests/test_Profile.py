from whalrus.profile.Profile import Profile
from whalrus.ballot.BallotOrder import BallotOrder


def test():
    # Conversion to str
    profile = Profile(
        ballots=['a > b ~ c', 'a ~ b > c'],
        voters=['Alice', None],
        weights=[1, 2]
    )
    assert str(profile) == 'Alice (1): a > b ~ c\nNone (2): a ~ b > c'
    profile = Profile(
        ballots=['a > b ~ c', 'a ~ b > c'],
        voters=['Alice', None]
    )
    assert str(profile) == 'Alice: a > b ~ c\nNone: a ~ b > c'
    profile = Profile(
        ballots=['a > b ~ c', 'a ~ b > c'],
        weights=[1, 2]
    )
    assert str(profile) == '(1): a > b ~ c\n(2): a ~ b > c'
    profile = Profile(
        ballots=['a > b ~ c', 'a ~ b > c']
    )
    assert str(profile) == 'a > b ~ c\na ~ b > c'

    # Misc...
    profile = Profile(
        ballots=['a > b ~ c', 'a ~ b > c'],
        weights=[2, 1],
        voters=['Alice', 'Bob']
    )
    assert repr(profile) == "Profile(ballots=[BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'}), " \
                            "BallotOrder([{'a', 'b'}, 'c'], candidates={'a', 'b', 'c'})], " \
                            "weights=[2, 1], voters=['Alice', 'Bob'])"
    assert profile.ballots == [BallotOrder('a > b ~ c'), BallotOrder('a ~ b > c')]
    assert profile.weights == [2, 1]
    assert profile.voters == ['Alice', 'Bob']
    assert profile.has_weights
    assert profile.has_voters
    assert len(profile) == 2
    assert profile[0] == BallotOrder('a > b ~ c')
    profile[0] = 'a > b > c'
    assert profile[0] == BallotOrder('a > b > c')
    del profile[0]
    assert str(profile) == 'Bob: a ~ b > c'

    # Append and remove
    profile = Profile([])
    profile.append('a > b ~ c')
    assert repr(profile) == "Profile(ballots=[BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})], " \
                            "weights=[1], voters=[None])"
    profile = Profile([])
    profile.append('a > b ~ c', weight=3, voter='Alice')
    assert repr(profile) == "Profile(ballots=[BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})], " \
                            "weights=[3], voters=['Alice'])"
    profile.remove(voter='Alice')
    assert repr(profile) == "Profile(ballots=[], weights=[], voters=[])"

    # Concatenate and multiply
    profile = Profile(
        ballots=['a > b ~ c'],
        voters=['Alice'],
        weights=[2]
    )
    profile += ['b > c > a', 'c > a > b']
    assert str(profile) == 'Alice (2): a > b ~ c\nNone (1): b > c > a\nNone (1): c > a > b'
    profile *= 3
    assert str(profile) == 'Alice (6): a > b ~ c\nNone (3): b > c > a\nNone (3): c > a > b'
