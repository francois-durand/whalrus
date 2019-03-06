from whalrus.rule.RulePlurality import RulePlurality
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.rule.RuleIteratedElimination import RuleIteratedElimination
from whalrus.priority.Priority import Priority
from whalrus.profile.Profile import Profile
from whalrus.ballot.BallotOrder import BallotOrder


def quick_start():
    """
    Simple elections:

    >>> RulePlurality(['a', 'a', 'b', 'c']).winner_
    'a'
    >>> RuleBorda(['a ~ b > c', 'b > c > a']).scores_
    {'a': 1.5, 'b': 3.5, 'c': 1.0}

    Elections with weights, voter names:

    >>> RulePlurality(
    ...     ['a', 'a', 'b', 'c'], weights=[1, 1, 3, 2],
    ...     voters=['Alice', 'Bob', 'Cat', 'Dave']
    ... ).winner_
    'b'

    Choosing the tie-breaking rule:

    >>> RulePlurality(['a', 'a', 'b', 'b', 'c'], tie_break=Priority.ASCENDING).winner_
    'a'
    """
    pass


def computed_attributes():
    """
    >>> plurality = RulePlurality(['a', 'a', 'b', 'b', 'c'], tie_break=Priority.ASCENDING)
    >>> plurality.candidates_
    {'a', 'b', 'c'}
    >>> plurality.scores_
    {'a': 2, 'b': 2, 'c': 1}
    >>> plurality.best_score_
    2
    >>> plurality.worst_score_
    1
    >>> plurality.order_
    [{'a', 'b'}, {'c'}]
    >>> plurality.strict_order_
    ['a', 'b', 'c']
    >>> plurality.cowinners_
    {'a', 'b'}
    >>> plurality.winner_
    'a'
    >>> plurality.cotrailers_
    {'c'}
    >>> plurality.trailer_
    'c'
    """
    pass


def general_syntax():
    """
    In the most general syntax, firstly, you define the rule and enter its options:

    >>> plurality = RulePlurality(tie_break=Priority.ASCENDING)

    Secondly, you use it as a callable to load a particular election (profile, set of candidates):

    >>> plurality(ballots=['a', 'b', 'c'], weights=[2, 2, 1], voters=['Alice', 'Bob', 'Cat'],
    ...           candidates={'a', 'b', 'c', 'd'})  # doctest:+ELLIPSIS
    <whalrus.rule.RulePlurality.RulePlurality object at ...>

    Finally, you can access the computed variables:

    >>> plurality.scores_
    {'a': 2, 'b': 2, 'c': 1, 'd': 0}

    Later, if you wish, you can load another profile with the same voting rule, and so on.
    """
    pass


def under_the_hood():
    """
    Internally, a voting rule is always applied to a :class:`Profile`. A :class:`Profile` contains a list of
    :class:`Ballot` objects, a list of weights and a list of voters. A :class:`Ballot` contains the message emitted
    by the voter, but also some contextual information such as the set of candidates that were available at the moment
    when she cast her ballot: this architecture allows Whalrus to deal with asynchronous elections where the set
    of candidates may vary during the election itself (such as some asynchronous online polls).

    >>> borda = RuleBorda()
    >>> borda(['a > b ~ c', 'a ~ b > c'])  # doctest:+ELLIPSIS
    <whalrus.rule.RuleBorda.RuleBorda object at ...>
    >>> borda.profile_converted_
    Profile(ballots=[BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'}), BallotOrder([{'a', 'b'}, 'c'], candidates={'a', 'b', 'c'})], weights=[1, 1], voters=[None, None])

    And for example, the first ballot is:

    >>> borda.profile_converted_[0]
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})

    Under the hood, some conversions are performed so that a variety of inputs are understood by Whalrus. In the
    example above, the first ballot was manually entered as 'a > b ~ c'. In the absence of other information, Whalrus
    then considered that only candidates a, b and c were available when this voter cast her ballot. If you want to give
    more detailed information, the most general syntax consists in using the constructors of classes :class:`Profile`,
    :class:`Ballot` and their subclasses.

    >>> a_more_complex_ballot = BallotOrder('a > b ~ c', candidates={'a', 'b', 'c', 'd', 'e'})

    The type of ballot above means that the voter emitted the message 'a > b ~ c' in a context where the candidates
    d and e where also available, thus abstaining about these two candidates.
    """


def combine_rules():
    """
    It is possible to combine some rules to obtain new rules.

    >>> irv = RuleIteratedElimination(base_rule=RulePlurality())
    >>> irv(['a > b > c', 'b > a > c', 'c > a > b'],
    ...     weights=[2, 3, 4]).winner_
    'b'

    Cf. also :class:`RuleSequentialTieBreak` for example.
    """


def change_candidates():
    """
    It is also possible to change the set of candidates, compared to when the voters cast their ballots.

    >>> profile = Profile(['a > b > c', 'a ~ b > c'])
    >>> RulePlurality(profile, candidates={'b', 'c'}).scores_
    {'b': 2, 'c': 0}
    """
