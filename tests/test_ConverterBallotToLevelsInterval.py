from whalrus.converter_ballot.ConverterBallotToLevelsInterval import ConverterBallotToLevelsInterval
from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.scale.ScaleInterval import ScaleInterval


def test():
    converter = ConverterBallotToLevelsInterval()
    assert converter({'a': 10, 'b': 7, 'c': 0}) == BallotLevels(
        {'a': 1.0, 'b': 0.7, 'c': 0.0}, candidates={'a', 'b', 'c'}, scale=ScaleInterval(low=0.0, high=1.0))
    assert converter({'a': .7, 'b': .3}) == BallotLevels({'a': .7, 'b': .3}, scale=ScaleInterval(low=0., high=1.))
    assert converter({'a': 1., 'b': 0., 'c': -1.}) == BallotLevels(
        {'a': 1., 'b': .5, 'c': 0.}, scale=ScaleInterval(low=0., high=1.))
    assert converter({'a': 'A', 'b': 'B', 'c': 'C'}) == BallotLevels(
        {'a': 0., 'b': .5, 'c': 1.}, scale=ScaleInterval(low=0., high=1.))
