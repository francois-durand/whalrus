import pytest
from whalrus import ConverterBallotGeneral
from whalrus import BallotOneName


def test():
    converter = ConverterBallotGeneral()
    assert repr(converter('c', {'a', 'b', 'd'})) == "BallotOneName(None, candidates={})"
    with pytest.raises(ValueError):
        _ = converter(BallotOneName('c', candidates={'a', 'b', 'c'}), candidates={'a', 'b', 'd'})
