from whalrus.converter_ballot.ConverterBallot import ConverterBallot
from whalrus.converter_ballot.ConverterBallotGeneral import ConverterBallotGeneral
from whalrus.ballot.Ballot import Ballot
from whalrus.ballot.BallotPlurality import BallotPlurality
from whalrus.ballot.BallotVeto import BallotVeto
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.ballot.BallotOrder import BallotOrder
from whalrus.priority.Priority import Priority


class ConverterBallotToVeto(ConverterBallot):
    """
    Default converter to veto ballot.

    :param order_priority: option passed to :meth:`BallotOrder.last`.
    :param plurality_priority: option passed to :meth:`BallotPlurality.last`.
    :param veto_priority: option passed to :meth:`BallotVeto.last`.
    :param one_name_priority: option passed to :meth:`BallotOneName.last`.

    This is a default converter to a veto ballot. It tries to infer the type of input and converts it to
    a veto ballot.

    Typical usages:

    >>> converter = ConverterBallotToVeto()
    >>> converter(BallotOneName('a', candidates={'a', 'b'}))
    BallotVeto('a', candidates={'a', 'b'})
    >>> converter(BallotPlurality('a', candidates={'a', 'b'}))
    BallotVeto('b', candidates={'a', 'b'})
    >>> converter({'a': 10, 'b': 7, 'c':0})
    BallotVeto('c', candidates={'a', 'b', 'c'})
    >>> converter('a ~ b > c')
    BallotVeto('c', candidates={'a', 'b', 'c'})
    >>> converter([{'a', 'b'}, 'c'])
    BallotVeto('c', candidates={'a', 'b', 'c'})

    Use options for the restrictions:

    >>> converter = ConverterBallotToVeto(order_priority=Priority.ASCENDING)
    >>> converter(BallotOrder('a > b ~ c'))
    BallotVeto('c', candidates={'a', 'b', 'c'})
    """

    def __init__(self,
                 order_priority: Priority = Priority.UNAMBIGUOUS,
                 plurality_priority: Priority = Priority.UNAMBIGUOUS,
                 veto_priority: Priority = Priority.UNAMBIGUOUS,
                 one_name_priority: Priority = Priority.UNAMBIGUOUS):
        self.order_priority = order_priority
        self.plurality_priority = plurality_priority
        self.veto_priority = veto_priority
        self.one_name_priority = one_name_priority

    def __call__(self, x: object, candidates: set = None) -> BallotVeto:
        x = ConverterBallotGeneral()(x, candidates=None)
        if isinstance(x, BallotPlurality):
            last = x.last(candidates=candidates, priority=self.plurality_priority)
            if candidates is None:
                candidates = x.candidates
            else:
                candidates = x.candidates & candidates
            return BallotVeto(last, candidates=candidates)
        if isinstance(x, BallotVeto):
            return x.restrict(candidates=candidates, priority=self.veto_priority)
        if isinstance(x, BallotOneName):
            x = BallotVeto(x.candidate, candidates=x.candidates)
            return x.restrict(candidates=candidates, priority=self.one_name_priority)
        if isinstance(x, BallotOrder):
            x = x.restrict(candidates=candidates)
            return BallotVeto(x.last(priority=self.order_priority), candidates=x.candidates)
        if isinstance(x, Ballot):
            x = ConverterBallotGeneral()(x, candidates=candidates)
            return BallotVeto(x.last(), candidates=x.candidates)
