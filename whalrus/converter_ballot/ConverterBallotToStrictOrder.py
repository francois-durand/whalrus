from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotToOrder import ConverterBallotToOrder
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.priority.Priority import Priority
from itertools import chain


class ConverterBallotToStrictOrder(ConverterBallot):
    """
    Default converter to a strictly ordered ballot.

    This is a default converter to a strictly ordered ballot. It tries to infer the type of input and converts
    it to a strictly ordered ballot (possibly a ballot of a subclass, such as :class:`BallotLevels`).

    Typical usages:

    >>> converter = ConverterBallotToStrictOrder(priority=Priority.ASCENDING)
    >>> converter('a > b ~ c')
    BallotOrder(['a', 'b', 'c'], candidates={'a', 'b', 'c'})
    >>> converter(['a', {'b', 'c'}])
    BallotOrder(['a', 'b', 'c'], candidates={'a', 'b', 'c'})
    >>> converter({'a': 10, 'b': 7, 'c': 0})
    BallotLevels({'a': 10, 'b': 7, 'c': 0}, candidates={'a', 'b', 'c'}, scale=Scale())
    >>> converter(BallotOneName('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['a', 'b', 'c'], candidates={'a', 'b', 'c'})
    >>> converter(BallotPlurality('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['a', 'b', 'c'], candidates={'a', 'b', 'c'})
    >>> converter(BallotVeto('a', candidates={'a', 'b', 'c'}))
    BallotOrder(['b', 'c', 'a'], candidates={'a', 'b', 'c'})
    """

    def __init__(self, priority: Priority = Priority.UNAMBIGUOUS):
        self.priority = priority

    def __call__(self, x: object, candidates: set = None) -> BallotOrder:
        x = ConverterBallotToOrder()(x, candidates=candidates)
        if x.is_strict:
            return x
        else:
            return BallotOrder(list(chain(*[
                self.priority.sort(indifference_class) for indifference_class in x.as_weak_order
            ])))
