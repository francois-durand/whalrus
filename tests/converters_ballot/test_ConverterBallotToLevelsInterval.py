from whalrus import ConverterBallotToLevelsInterval, BallotLevels, ScaleInterval, BallotOneName, BallotVeto
from fractions import Fraction


def test():
    converter = ConverterBallotToLevelsInterval()
    assert converter({'a': 10, 'b': 7, 'c': 0}) == BallotLevels(
        {'a': 1, 'b': Fraction(7, 10), 'c': 0}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(low=0, high=1))
    assert converter({'a': .7, 'b': .3}) == BallotLevels(
        {'a': Fraction(7, 10), 'b': Fraction(3, 10)}, scale=ScaleInterval(low=0, high=1))
    assert converter({'a': 1, 'b': 0, 'c': -1}) == BallotLevels(
        {'a': 1, 'b': Fraction(1, 2), 'c': 0}, scale=ScaleInterval(low=0, high=1))
    assert converter({'a': 'A', 'b': 'B', 'c': 'C'}) == BallotLevels(
        {'a': 0, 'b': Fraction(1, 2), 'c': 1}, scale=ScaleInterval(low=0, high=1))


def test_ballot_one_name_abstention():
    """
        >>> converter = ConverterBallotToLevelsInterval()
        >>> ballot = BallotOneName(None, candidates={'a', 'b', 'c'})
        >>> converter(ballot)
        BallotLevels({}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(low=0, high=1))
        >>> ballot = BallotVeto(None, candidates={'a', 'b', 'c'})
        >>> converter(ballot)
        BallotLevels({}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(low=0, high=1))
    """
    pass
