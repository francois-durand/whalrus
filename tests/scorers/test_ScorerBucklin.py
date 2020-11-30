from whalrus import ScorerBucklin, BallotOrder


def test():
    """
        >>> scorer = ScorerBucklin(k=3, absent_receive_points=False)
        >>> ballot = BallotOrder('a > b')
        >>> scorer(ballot, candidates={'a', 'b', 'c', 'd'}).scores_as_floats_
        {'a': 1.0, 'b': 1.0, 'c': 0.0, 'd': 0.0}
    """
    pass
