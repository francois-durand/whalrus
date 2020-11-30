from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
from whalrus.ballots.ballot_one_name import BallotOneName
from whalrus.ballots.ballot_order import BallotOrder
from whalrus.ballots.ballot_veto import BallotVeto


def test():
    converter = ConverterBallotToOrder()
    assert converter(BallotOneName('a', candidates={'a', 'b', 'c'}), candidates={'b', 'c', 'd'}) == BallotOrder(
        'b ~ c', candidates={'b', 'c'}
    )
    assert converter(BallotVeto('a', candidates={'a', 'b', 'c'}), candidates={'b', 'c', 'd'}) == BallotOrder(
        'b ~ c', candidates={'b', 'c'}
    )
