import pytest
from whalrus import ConverterBallotToLevelsListNumeric, ScaleFromList, BallotLevels


def test_scale_non_numeric():
    converter = ConverterBallotToLevelsListNumeric(scale=ScaleFromList(['Bad', 'Medium', 'Good']))
    ballot = BallotLevels({'a': 10, 'b': 7, 'c': 0})
    with pytest.raises(ValueError):
        converter(ballot)
