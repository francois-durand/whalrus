from whalrus.ballot.Ballot import Ballot
from whalrus.scale.Scale import Scale
from whalrus.utils.Utils import DeleteCacheMixin, cached_property, NiceDict


class Scorer(DeleteCacheMixin):
    """
    A `scorer'.

    :param ballot: if mentioned, will be passed to `__call__` immediately after initialization.
    :param voter: if mentioned, will be passed to `__call__` immediately after initialization.
    :param candidates: if mentioned, will be passed to `__call__` immediately after initialization.
    :param scale: the scale in which scores are computed.

    A :class:`Scorer` is a callable whose inputs are a ballot, a voter and a set of candidates (the set of candidates
    of the election).  When the scorer is called, it loads its arguments. The output of the call is the scorer
    itself. But after the call, you can access to the computed variables (ending with an underscore),
    such as :attr:`scores_`.

    At the initialization of a :class:`Scorer` object, some options can be given, such as a scale. In some
    subclasses, there can be some additional options.

    Cf. :class:`ScorerLevels` for some examples.
    """

    def __init__(self, ballot: Ballot = None, voter: object = None, candidates: set = None,
                 scale: Scale = None):
        if scale is None:
            scale = Scale()
        # Parameters
        self.scale = scale
        # Computed variables
        self.ballot_ = None
        self.voter_ = None
        self.candidates_ = None
        # Optional: load a ballot at initialization
        if ballot is not None:
            self(ballot=ballot, voter=voter, candidates=candidates)

    def __call__(self, ballot: Ballot, voter: object = None, candidates: set = None):
        """
        Load the arguments.

        :param ballot: a ballot. We assume that it is already in the correct subclass of :class:`Ballot` and that it is
            already restricted to the candidates of the election (if necessary).
        :param voter: the voter.
        :param candidates: the candidates.
        """
        self.ballot_ = ballot
        self.voter_ = voter
        self.candidates_ = candidates
        self.delete_cache()
        return self

    @cached_property
    def scores_(self) -> NiceDict:
        """
        The scores.

        :return: a :class:`NiceDict` that, to each candidate, associates either a level in the scale or None.
            For the meaning of None, cf. :class:`RuleRangeVoting` for example. Intuitively: a score of 0 means that 0
            is counted (as 0) in the average, whereas None is not counted at all (i.e. the weight of the voter
            is not even counted in the denominator when computing the average).
        """
        raise NotImplementedError
