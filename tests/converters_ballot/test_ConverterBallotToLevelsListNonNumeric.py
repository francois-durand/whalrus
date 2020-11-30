import logging
from whalrus import ConverterBallotToLevelsListNonNumeric, ScaleFromList, BallotLevels

LOGGER = logging.getLogger(__name__)


def test(caplog):
    # The following case is disturbing, hence the warning.
    # * In `ballot`, 'a' is 'Good', which we would ideally like to keep as it is because this value is also present in
    #   the converter's scale.
    # * But 'b' is 'Quite bad', which denies using the same scale as the converter, or even a sub-scale.
    # In this sort of case, the decision is to do a "rescaling", i.e. do as if 'Good' in the ballot scale
    # has not the same meaning as in the converter's scale. Hence 'a' becomes 'Excellent' and 'b' becomes 'Bad'. But
    # a warning is issued.

    # LOGGER.info('Testing now.')
    ballot = BallotLevels({'a': 'Good', 'b': 'Quite bad'}, scale=ScaleFromList(['Quite bad', 'Good']))
    converter = ConverterBallotToLevelsListNonNumeric(
        scale=ScaleFromList(['Bad', 'Medium', 'Good', 'Very Good', 'Great', 'Excellent']))
    converted_ballot = converter(ballot)
    assert 'Not all levels' in caplog.text
    assert converted_ballot == BallotLevels(
        {'a': 'Excellent', 'b': 'Bad'}, candidates={'a', 'b'},
        scale=ScaleFromList(levels=['Bad', 'Medium', 'Good', 'Very Good', 'Great', 'Excellent'])
    )

    # You can compare with the following behavior, when 'ballot' uses a sub-scale of the converter's scale.
    # In that case, no "rescaling" is done: the levels are kept as they are.
    ballot = BallotLevels({'a': 'Good', 'b': 'Medium'})
    converter = ConverterBallotToLevelsListNonNumeric(
        scale=ScaleFromList(['Bad', 'Medium', 'Good', 'Very Good', 'Great', 'Excellent']))
    converted_ballot = converter(ballot)
    assert converted_ballot == BallotLevels(
        {'a': 'Good', 'b': 'Medium'}, candidates={'a', 'b'},
        scale=ScaleFromList(levels=['Bad', 'Medium', 'Good', 'Very Good', 'Great', 'Excellent'])
    )
