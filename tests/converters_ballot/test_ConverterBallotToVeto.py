import pytest
from whalrus import ConverterBallotToVeto, BallotPlurality, BallotOrder, BallotVeto, Ballot


def test_plurality_ballot():
    """
        >>> ballot = BallotPlurality('a', candidates={'a', 'b', 'c'})
        >>> converter = ConverterBallotToVeto()
        >>> converter(ballot, candidates={'a', 'b', 'd'})
        BallotVeto('b', candidates={'a', 'b'})
    """
    pass


def test_veto_ballot():
    """
        >>> ballot = BallotVeto('a', candidates={'a', 'b', 'c'})
        >>> converter = ConverterBallotToVeto()
        >>> converter(ballot, candidates={'a', 'b'})
        BallotVeto('a', candidates={'a', 'b'})
    """
    pass


def test_ballot_of_other_subclass():
    converter = ConverterBallotToVeto()
    ballot = Ballot()
    with pytest.raises(NotImplementedError):
        converter(ballot)
