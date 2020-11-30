import pytest
from whalrus import ConverterBallotToPlurality, BallotPlurality, BallotOrder, BallotVeto, Ballot


def test():
    converter = ConverterBallotToPlurality()
    assert str(converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))) == 'a'
    assert repr(converter(BallotOrder('a > b ~ c'))) == "BallotPlurality('a', candidates={'a', 'b', 'c'})"


def test_veto_ballot():
    """
        >>> ballot = BallotVeto('a', candidates={'a', 'b', 'c'})
        >>> converter = ConverterBallotToPlurality()
        >>> converter(ballot, candidates={'a', 'b', 'd'})
        BallotPlurality('b', candidates={'a', 'b'})
    """
    pass


def test_ballot_of_other_subclass():
    converter = ConverterBallotToPlurality()
    ballot = Ballot()
    with pytest.raises(NotImplementedError):
        converter(ballot)
