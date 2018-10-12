from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.ballot.BallotVeto import BallotVeto


def test():
    converter = ConverterBallotToOrder()
    assert converter(BallotOneName('a', candidates={'a', 'b', 'c'}), candidates={'b', 'c', 'd'}) == BallotOrder(
        'b ~ c', candidates={'b', 'c'}
    )
    assert converter(BallotVeto('a', candidates={'a', 'b', 'c'}), candidates={'b', 'c', 'd'}) == BallotOrder(
        'b ~ c', candidates={'b', 'c'}
    )
