from whalrus import ConverterBallotToLevels, BallotLevels, BallotOrder


def test():
    """
        >>> converter = ConverterBallotToLevels()
        >>> ballot = BallotLevels({'a': 10, 'b': 7, 'c': 0})
        >>> converter(ballot)
        BallotLevels({'a': 10, 'b': 7, 'c': 0}, candidates={'a', 'b', 'c'}, scale=Scale())
        >>> ballot = BallotOrder('a > b > c')
        >>> converter(ballot)
        BallotLevels({'a': 1, 'b': Fraction(1, 2), 'c': 0}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(low=0, high=1))
    """
    pass
