from whalrus.converter_ballot.ConverterBallotToPlurality import ConverterBallotToPlurality
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOrder import BallotOrder


def test():
    converter = ConverterBallotToPlurality()
    assert str(converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))) == 'a'
    assert repr(converter(BallotOrder('a > b ~ c'))) == "BallotPlurality('a', candidates={'a', 'b', 'c'})"
