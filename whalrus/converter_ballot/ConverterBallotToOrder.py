from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOrder import BallotOrder


class ConverterBallotToOrder(ConverterBallot):
    """
    Default converter to an ordered ballot.

    This is a default converter to an ordered ballot. It tries to infer the type of input and converts it to
    an ordered ballot (possibly a ballot of a subclass, such as :class:`BallotLevels`).

    Typical usages:

    >>> converter = ConverterBallotToOrder()
    >>> converter('a > b ~ c')
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> converter(['a', {'b', 'c'}])
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> converter({'a': 10, 'b': 7, 'c': 0})
    BallotLevels({'a': 10, 'b': 7, 'c': 0}, candidates={'a', 'b', 'c'}, scale=Scale())
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'}))
    BallotOrder([{'b', 'c'}, 'a'], candidates={'a', 'b', 'c'})
    """

    def __call__(self, x: object, candidates: set = None) -> BallotOrder:
        x = ConverterBallotGeneral()(x, candidates=None)
        if isinstance(x, BallotOrder):
            return x.restrict(candidates=candidates)
        if isinstance(x, BallotVeto):
            return BallotOrder([x.candidates_not_in_b, {x.last()}]).restrict(candidates=candidates)
        if isinstance(x, BallotOneName):
            return BallotOrder([{x.first()}, x.candidates_not_in_b]).restrict(candidates=candidates)
        raise NotImplementedError
