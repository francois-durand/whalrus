import pytest
from whalrus import ScorerLevels, BallotLevels, ScaleFromList


def test():
    scorer = ScorerLevels()
    ballot = BallotLevels({'a': 'Good', 'b': 'Bad'}, scale=ScaleFromList(['Bad', 'Good']))
    with pytest.raises(ValueError):
        _ = scorer(ballot).scores_as_floats_
