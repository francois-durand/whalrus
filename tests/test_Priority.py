from whalrus import Priority
import pytest


def test_two_elements_or_more():
    my_set = {'d', 'b', 'a', 'c'}

    priority = Priority.UNAMBIGUOUS
    with pytest.raises(ValueError):
        _ = priority.choice(my_set)
    with pytest.raises(ValueError):
        _ = priority.choice(my_set, reverse=True)
    with pytest.raises(ValueError):
        _ = priority.sort(my_set)
    with pytest.raises(ValueError):
        _ = priority.sort(my_set, reverse=True)

    priority = Priority.ABSTAIN
    assert priority.choice(my_set) is None
    assert priority.choice(my_set, reverse=True) is None
    assert priority.sort(my_set) is None
    assert priority.sort(my_set, reverse=True) is None

    priority = Priority.ASCENDING
    assert priority.choice(my_set) == 'a'
    assert priority.choice(my_set, reverse=True) == 'd'
    assert priority.sort(my_set) == ['a', 'b', 'c', 'd']
    assert priority.sort(my_set, reverse=True) == ['d', 'c', 'b', 'a']

    priority = Priority.DESCENDING
    assert priority.choice(my_set) == 'd'
    assert priority.choice(my_set, reverse=True) == 'a'
    assert priority.sort(my_set) == ['d', 'c', 'b', 'a']
    assert priority.sort(my_set, reverse=True) == ['a', 'b', 'c', 'd']

    priority = Priority.RANDOM
    assert priority.choice(my_set) in my_set
    assert priority.choice(my_set, reverse=True) in my_set
    assert set(priority.sort(my_set)) == my_set
    assert set(priority.sort(my_set, reverse=True)) == my_set


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
