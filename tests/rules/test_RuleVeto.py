from whalrus import RuleVeto, ScorerPlurality, BallotPlurality, ScorerVeto, BallotVeto
import logging

LOGGER = logging.getLogger(__name__)


def test_scorer_not_plurality():
    """
    A strange voting rule where the candidate with least positive votes wins!

        >>> rule = RuleVeto(scorer=ScorerPlurality())
        >>> rule([BallotPlurality('a', candidates={'a', 'b'})]).winner_
        'b'
    """
    pass


def test_count_abstention():
    """
        >>> rule = RuleVeto(scorer=ScorerVeto(count_abstention=True))
        >>> rule(['a', 'a', 'b', None]).scores_
        {'a': Fraction(-1, 2), 'b': Fraction(-1, 4)}
    """
    pass


def test_check_profile(caplog):
    # LOGGER.info('Testing now.')
    rule = RuleVeto()
    rule([BallotVeto('a', candidates={'a', 'b'}), BallotVeto('b', candidates={'a', 'b', 'c'})])
    assert 'Some ballots do not have the same set of candidates as the whole election.' in caplog.text
