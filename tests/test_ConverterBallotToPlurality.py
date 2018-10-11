from whalrus.converters_ballot.ConverterBallotToPlurality import ConverterBallotToPlurality
from whalrus.ballots.BallotPlurality import BallotPlurality
from whalrus.ballots.BallotOrder import BallotOrder


def test():
    converter = ConverterBallotToPlurality()
    assert str(converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))) == 'a'
    assert repr(converter(BallotOrder('a > b ~ c'))) == "BallotPlurality('a', candidates={'a', 'b', 'c'})"
