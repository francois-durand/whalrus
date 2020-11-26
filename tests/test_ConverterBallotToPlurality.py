from whalrus.converters_ballot.converter_ballot_to_plurality import ConverterBallotToPlurality
from whalrus.ballots.ballot_plurality import BallotPlurality
from whalrus.ballots.ballot_order import BallotOrder


def test():
    converter = ConverterBallotToPlurality()
    assert str(converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))) == 'a'
    assert repr(converter(BallotOrder('a > b ~ c'))) == "BallotPlurality('a', candidates={'a', 'b', 'c'})"
