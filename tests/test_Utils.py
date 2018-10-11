import pytest
from pyparsing import ParseException
from whalrus.utils.Utils import parse_weak_order, set_to_str, dict_to_str


def test_parse_weak_order():
    assert parse_weak_order('') == []
    assert parse_weak_order('  ') == []
    with pytest.raises(ParseException):
        parse_weak_order('a * b')


def test_set_to_str():
    s = set_to_str({'a', 42})
    assert s == "{'a', 42}" or s == "{42, 'a'}"


def test_dict_to_str():
    s = dict_to_str({'a': 1, 51: 0})
    assert s == "{'a': 1, 51: 0}" or s == "{51: 0, 'a': 1}"
