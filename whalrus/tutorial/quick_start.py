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
