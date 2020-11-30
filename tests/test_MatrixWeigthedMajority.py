from whalrus import MatrixWeightedMajority, BallotOrder, Profile


def test():
    """
        >>> matrix = MatrixWeightedMajority(ordered_vs_unordered=51, unordered_vs_ordered=42)
        >>> ballot = BallotOrder('a > b', candidates={'a', 'b', 'c'})
        >>> matrix([ballot]).as_array_
        array([[ 0,  1, 51],
               [ 0,  0, 51],
               [42, 42,  0]])

        >>> matrix = MatrixWeightedMajority(ordered_vs_absent=51, absent_vs_ordered=42)
        >>> ballot = BallotOrder('a > b')
        >>> matrix([ballot], candidates={'a', 'b', 'c'}).as_array_
        array([[ 0,  1, 51],
               [ 0,  0, 51],
               [42, 42,  0]])

        >>> matrix = MatrixWeightedMajority(unordered_vs_unordered =42)
        >>> ballot = BallotOrder('a > b', candidates={'a', 'b', 'c', 'd'})
        >>> matrix([ballot]).as_array_
        array([[ 0,  1,  1,  1],
               [ 0,  0,  1,  1],
               [ 0,  0,  0, 42],
               [ 0,  0, 42,  0]])

        >>> matrix = MatrixWeightedMajority(unordered_vs_absent=51, absent_vs_unordered=42)
        >>> ballot = BallotOrder('a > b', candidates={'a', 'b', 'c'})
        >>> matrix([ballot], candidates={'a', 'b', 'c', 'd'}).as_array_
        array([[ 0,  1,  1,  0],
               [ 0,  0,  1,  0],
               [ 0,  0,  0, 51],
               [ 0,  0, 42,  0]])

        >>> matrix = MatrixWeightedMajority(absent_vs_absent=42)
        >>> ballot = BallotOrder('a > b')
        >>> matrix([ballot], candidates={'a', 'b', 'c', 'd'}).as_array_
        array([[ 0,  1,  0,  0],
               [ 0,  0,  0,  0],
               [ 0,  0,  0, 42],
               [ 0,  0, 42,  0]])
    """
    pass
