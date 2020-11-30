from whalrus import Matrix, ConverterBallotGeneral
import logging

LOGGER = logging.getLogger(__name__)


def test():
    """
        >>> matrix = Matrix()
        >>> type(matrix.converter) == ConverterBallotGeneral
        True
    """
    pass


def test_check_profile(caplog):
    # LOGGER.info('Testing now.')
    matrix = Matrix()
    matrix(['a > b > c', 'a > b'])
    assert 'Some ballots do not have the same set of candidates as the whole election.' in caplog.text
