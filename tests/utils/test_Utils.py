import pytest
from pyparsing import ParseException
from whalrus.utils.utils import parse_weak_order, set_to_str, dict_to_str, set_to_list, dict_to_items, take_closest, \
    my_division


def test_parse_weak_order():
    assert parse_weak_order('') == []
    assert parse_weak_order('  ') == []
    with pytest.raises(ParseException):
        parse_weak_order('a * b')


def test_set_to_list():
    not_sortable_variable = 42
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        _ = set_to_list(not_sortable_variable)


def test_set_to_str():
    s = set_to_str({'a', 42})
    assert s == "{'a', 42}" or s == "{42, 'a'}"


def test_dict_to_items():
    """
        >>> dict_to_items({'a': 10, 42: 0})
        [('a', 10), (42, 0)]
    """
    pass


def test_dict_to_str():
    s = dict_to_str({'a': 1, 51: 0})
    assert s == "{'a': 1, 51: 0}" or s == "{51: 0, 'a': 1}"


def test_take_closest():
    """
        >>> take_closest([0, 5, 10], 11)
        10
    """
    pass


def test_my_division():
    with pytest.raises(ZeroDivisionError):
        _ = my_division(1, 0)
    with pytest.raises(NotImplementedError):
        # noinspection PyTypeChecker
        _ = my_division(1, 'a')
