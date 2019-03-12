from whalrus.ballot.BallotLevels import BallotLevels
from whalrus.scale.Scale import Scale
from whalrus.utils.Utils import cached_property, NiceDict
from whalrus.scorer.Scorer import Scorer


class ScorerLevels(Scorer):
    """
    A standard scorer for :BallotLevel: objects.

    :param level_ungraded: the level of the scale used for ungraded candidates, or None.
    :param level_absent: the level of the scale used for absent candidates, or None.

    In the most general syntax, firstly, you define the scorer:

    >>> scorer = ScorerLevels(level_absent=0)

    Secondly, you use it as a callable to load some particular arguments:

    >>> scorer(ballot=BallotLevels({'a': 10, 'b': 7, 'c': 3}), voter='Alice', candidates={'a', 'b', 'c', 'd'})  # doctest:+ELLIPSIS
    <ScorerLevels.ScorerLevels object at ...>

    Finally, you can access the computed variables:

    >>> scorer.scores_
    {'a': 10, 'b': 7, 'c': 3, 'd': 0}

    Later, if you wish, you can load other arguments (ballot, etc) with the same scorer, and so on.

    Optionally, you can specify arguments as soon as the :class:`Scorer` object is initialized. This allows for
    one-liners such as:

    >>> ScorerLevels(ballot=BallotLevels({'a': 10, 'b': 7, 'c': 3}), voter='Alice', candidates={'a', 'b', 'c', 'd'},
    ...              level_absent=0).scores_
    {'a': 10, 'b': 7, 'c': 3, 'd': 0}

    In the example below, candidates ``a``, ``b`` and ``c`` are `ordered', ``d`` is `unordered', and ``e`` is `absent'
    in the ballot, meaning that ``e`` were not even available when the voter cast her ballot. The options of the
    scorer provide different ways to take these special cases into account.

    >>> ballot=BallotLevels({'a': 10, 'b': 7, 'c': 3}, candidates={'a', 'b', 'c', 'd'})
    >>> candidates_election = {'a', 'b', 'c', 'd', 'e'}
    >>> ScorerLevels(ballot, candidates=candidates_election).scores_
    {'a': 10, 'b': 7, 'c': 3}
    >>> ScorerLevels(ballot, candidates=candidates_election, level_ungraded=-5).scores_
    {'a': 10, 'b': 7, 'c': 3, 'd': -5}
    >>> ScorerLevels(ballot, candidates=candidates_election, level_ungraded=-5, level_absent=-10).scores_
    {'a': 10, 'b': 7, 'c': 3, 'd': -5, 'e': -10}
    """

    def __init__(self, ballot: BallotLevels = None, voter: object = None, candidates: set = None,
                 scale: Scale = None,
                 level_ungraded: object = None, level_absent: object = None):
        self.level_ungraded = level_ungraded
        self.level_absent = level_absent
        super().__init__(ballot=ballot, voter=voter, candidates=candidates, scale=scale)

    @cached_property
    def scores_(self) -> NiceDict:
        scores = NiceDict(self.ballot_.as_dict.copy())
        if self.level_absent is not None:
            scores.update({c: self.level_absent for c in self.candidates_ - self.ballot_.candidates})
        if self.level_ungraded is not None:
            scores.update({c: self.level_ungraded for c in self.ballot_.candidates_not_in_b})
        return scores
