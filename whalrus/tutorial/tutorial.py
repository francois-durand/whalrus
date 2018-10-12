from whalrus.rule.RulePlurality import RulePlurality
from whalrus.rule.RuleBorda import RuleBorda
from whalrus.priority.Priority import Priority


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
