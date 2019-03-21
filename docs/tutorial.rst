========
Tutorial
========

    >>> from whalrus import *

Quick start
===========

Some simple elections:

    >>> RulePlurality(['a', 'a', 'b', 'c']).winner_
    'a'
    >>> RuleBorda(['a > b > c', 'b > c > a']).gross_scores_
    {'a': 2, 'b': 3, 'c': 1}

Elections can optionally have weights and voter names:

    >>> RulePlurality(
    ...     ['a', 'a', 'b', 'c'], weights=[1, 1, 3, 2],
    ...     voters=['Alice', 'Bob', 'Cate', 'Dave']
    ... ).winner_
    'b'

The tie-breaking rule can be specified:

    >>> RulePlurality(['a', 'a', 'b', 'b', 'c'], tie_break=Priority.ASCENDING).winner_
    'a'

Computed attributes of an election
==================================

    >>> plurality = RulePlurality(['a', 'a', 'b', 'b', 'c'], tie_break=Priority.ASCENDING)

    Once the election is defined, you can access its computed attributes, whose names end with an underscore:

    >>> plurality.candidates_
    {'a', 'b', 'c'}
    >>> plurality.gross_scores_
    {'a': 2, 'b': 2, 'c': 1}
    >>> plurality.scores_
    {'a': Fraction(2, 5), 'b': Fraction(2, 5), 'c': Fraction(1, 5)}
    >>> plurality.best_score_
    Fraction(2, 5)
    >>> plurality.worst_score_
    Fraction(1, 5)
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

General syntax
==============

In the most general syntax, firstly, you define the rule and enter its options:

    >>> plurality = RulePlurality(tie_break=Priority.ASCENDING)

Secondly, you use it as a callable to load a particular election (profile, set of candidates):

    >>> plurality(ballots=['a', 'b', 'c'], weights=[2, 2, 1], voters=['Alice', 'Bob', 'Cate'],
    ...           candidates={'a', 'b', 'c', 'd'})  # doctest:+ELLIPSIS
    <... object at ...>

Finally, you can access the computed variables:

    >>> plurality.gross_scores_
    {'a': 2, 'b': 2, 'c': 1, 'd': 0}

Later, if you wish, you can load another profile with the same voting rule, and so on.

Under the hood
==============

A :class:`whalrus.Ballot` contains the message emitted by the voter, but also some contextual information such as the
set of candidates that were available at the moment when she cast her ballot:

    >>> ballot = BallotOrder('a > b ~ c')
    >>> ballot
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})

This architecture allows Whalrus to deal with asynchronous elections where the set of candidates may vary during the
election itself (such as some asynchronous online polls).

A :class:`whalrus.Profile` contains a list of :class:`whalrus.Ballot` objects, a list of weights and a list of voters:

    >>> profile = Profile(['a > b ~ c', 'a ~ b > c'])
    >>> profile.ballots[0]
    BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'})
    >>> profile.weights
    [1, 1]
    >>> profile.voters
    [None, None]

Internally, a voting rule is always applied to a :class:`whalrus.Profile`. Hence, if the inputs are given in a "loose"
format, they are converted to a :class:`whalrus.Profile`:

    >>> borda = RuleBorda(['a > b ~ c', 'a ~ b > c'])
    >>> borda.profile_converted_  # doctest:+ELLIPSIS
    Profile(ballots=[BallotOrder(['a', {'b', 'c'}], candidates={'a', 'b', 'c'}), ...)

Under the hood, some conversions are performed so that a variety of inputs are understood by Whalrus. In the
example above, the first ballot was manually entered as ``a > b ~ c``. In the absence of other information, Whalrus
then considered that only candidates `a`, `b` and `c` were available when this voter cast her ballot. If you want to
give more detailed information, the most general syntax consists in using the constructors of classes
:class:`whalrus.Profile`, :class:`whalrus.Ballot` and their subclasses:

    >>> a_more_complex_ballot = BallotOrder('a > b ~ c', candidates={'a', 'b', 'c', 'd', 'e'})

The ballot above means that the voter emitted the message 'a > b ~ c' in a context where the candidates
`d` and `e` where also available, i.e. she deliberately abstained about these two candidates.

Change the candidates
=====================

It is possible to change the set of candidates, compared to when the voters cast their ballots.

    >>> profile = Profile(['a > b > c', 'a ~ b > c'])
    >>> RulePlurality(profile, candidates={'b', 'c'}).gross_scores_
    {'b': 2, 'c': 0}
