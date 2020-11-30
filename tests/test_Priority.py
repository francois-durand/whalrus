from whalrus import Priority
import pytest


def test_two_elements_or_more():
    my_set = {'d', 'b', 'a', 'c'}

    priority = Priority.UNAMBIGUOUS
    assert repr(priority) == 'Priority.UNAMBIGUOUS'
    with pytest.raises(ValueError):
        _ = priority.compare('a', 'b')
    with pytest.raises(ValueError):
        _ = priority.choice(my_set)
    with pytest.raises(ValueError):
        _ = priority.choice(my_set, reverse=True)
    with pytest.raises(ValueError):
        _ = priority.sort(my_set)
    with pytest.raises(ValueError):
        _ = priority.sort(my_set, reverse=True)
    with pytest.raises(ValueError):
        _ = priority.sort_pairs_rp({('a', 'b'), ('b', 'a')})

    priority = Priority.ABSTAIN
    assert repr(priority) == 'Priority.ABSTAIN'
    assert priority.compare('a', 'b') is None
    assert priority.choice(my_set) is None
    assert priority.choice(my_set, reverse=True) is None
    assert priority.sort(my_set) is None
    assert priority.sort(my_set, reverse=True) is None
    assert priority.sort_pairs_rp({('a', 'b'), ('b', 'a')}) is None

    priority = Priority.ASCENDING
    assert repr(priority) == 'Priority.ASCENDING'
    assert priority.choice(my_set) == 'a'
    assert priority.choice(my_set, reverse=True) == 'd'
    assert priority.sort(my_set) == ['a', 'b', 'c', 'd']
    assert priority.sort(my_set, reverse=True) == ['d', 'c', 'b', 'a']

    priority = Priority.DESCENDING
    assert repr(priority) == 'Priority.DESCENDING'
    assert priority.choice(my_set) == 'd'
    assert priority.choice(my_set, reverse=True) == 'a'
    assert priority.sort(my_set) == ['d', 'c', 'b', 'a']
    assert priority.sort(my_set, reverse=True) == ['a', 'b', 'c', 'd']

    priority = Priority.RANDOM
    assert repr(priority) == 'Priority.RANDOM'
    assert priority.compare('a', 'a') == 0
    assert priority.compare('a', 'b') in {-1, 1}
    assert priority.choice(my_set) in my_set
    assert priority.choice(my_set, reverse=True) in my_set
    assert set(priority.sort(my_set)) == my_set
    assert set(priority.sort(my_set, reverse=True)) == my_set
    assert set(priority.sort_pairs_rp({('a', 'b'), ('b', 'a')})) == {('a', 'b'), ('b', 'a')}


def test_zero_element():
    my_set = set()
    priority = Priority.UNAMBIGUOUS
    assert priority.choice(my_set) is None
    assert priority.choice(my_set, reverse=True) is None
    assert priority.sort(my_set) == []
    assert priority.sort(my_set, reverse=True) == []


def test_one_element():
    my_set = {'a'}
    priority = Priority.UNAMBIGUOUS
    assert priority.choice(my_set) == 'a'
    assert priority.choice(my_set, reverse=True) == 'a'
    assert priority.sort(my_set) == ['a']
    assert priority.sort(my_set, reverse=True) == ['a']


def test_user_defined_priority():
    """
    We test if the default implementation of `choice` and `sort` works, because it is overridden in all the predefined
    subclasses:

        >>> class PriorityCustomAscending(Priority):
        ...     def __init__(self):
        ...         super().__init__(name='Custom Ascending Priority')
        ...     def compare(self, c, d):
        ...         if c == d:
        ...             return 0
        ...         return -1 if c < d else 1
        >>> priority = PriorityCustomAscending()
        >>> priority.choice({'a', 'b'})
        'a'
        >>> priority.choice({'a', 'b'}, reverse=True)
        'b'
        >>> priority.sort({'a', 'b'})
        ['a', 'b']
        >>> priority.sort({'a', 'b'}, reverse=True)
        ['b', 'a']
    """
    pass
