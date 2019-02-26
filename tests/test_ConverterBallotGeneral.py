import pytest
from whalrus import ConverterBallotGeneral
from whalrus import BallotOneName


def test():
    converter = ConverterBallotGeneral()
    assert repr(converter('c', {'a', 'b', 'd'})) == "BallotOneName(None, candidates={})"
    with pytest.raises(ValueError):
        _ = converter(BallotOneName('c', candidates={'a', 'b', 'c'}), candidates={'a', 'b', 'd'})
    assert repr(converter('a ~ b > c', candidates={'b', 'c', 'd'})) == "BallotOrder(['b', 'c'], candidates={'b', 'c'})"
    assert repr(converter({'a': 10, 'b': 7, 'c': 0}, candidates={'b', 'c', 'd'})
                ) == "BallotLevels({'b': 7, 'c': 0}, candidates={'b', 'c'}, scale=Scale())"
