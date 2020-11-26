from whalrus.converters_ballot.converter_ballot_to_levels_range import ConverterBallotToLevelsRange
from whalrus.ballots.ballot_levels import BallotLevels
from whalrus.scales.scale_range import ScaleRange


def test():
    converter = ConverterBallotToLevelsRange(scale=ScaleRange(low=0, high=10))
    assert converter({'a': 10, 'b': 7, 'c': 0}) == BallotLevels(
        {'a': 10, 'b': 7, 'c': 0}, candidates={'a', 'b', 'c'}, scale=ScaleRange(low=0, high=10))
    assert converter({'a': 7, 'b': 3}) == BallotLevels({'a': 7, 'b': 3},  scale=ScaleRange(low=0, high=10))
    assert converter({'a': 1, 'b': 0, 'c': -1}) == BallotLevels(
        {'a': 10, 'b': 5, 'c': 0}, scale=ScaleRange(low=0, high=10))
    assert converter({'a': 'A', 'b': 'B', 'c': 'C'}) == BallotLevels(
        {'a': 0, 'b': 5, 'c': 10},  scale=ScaleRange(low=0, high=10))
