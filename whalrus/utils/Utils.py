# -*- coding: utf-8 -*-
from pyparsing import Group, Word, ZeroOrMore, alphas, nums, ParseException
from bisect import bisect_left
from fractions import Fraction
from decimal import Decimal
from numbers import Number


def _cache(f):
    """
    Auxiliary decorator used by ``cached_property``.

    :param f: a method with no argument (except ``self``).
    :return: the same function, but with a `caching' behavior.
    """
    name = f.__name__

    # noinspection PyProtectedMember
    def _f(*args):
        try:
            return args[0]._cached_properties[name]
        except KeyError:
            # Not stored in cache
            value = f(*args)
            args[0]._cached_properties[name] = value
            return value
        except AttributeError:
            # cache does not even exist
            value = f(*args)
            args[0]._cached_properties = {name: value}
            return value
    _f.__doc__ = f.__doc__
    return _f


def cached_property(f):
    """
    Decorator used in replacement of @property to put the value in cache automatically.

    The first time the attribute is used, it is computed on-demand and put in cache. Later accesses to the
    attributes will use the cached value.

    Cf. :class:`DeleteCacheMixin` for an example.
    """
    return property(_cache(f))


class DeleteCacheMixin:
    """
    Mixin used to delete cached properties.

    Cf. decorator :meth:`cached_property`.

    >>> class Example(DeleteCacheMixin):
    ...     @cached_property
    ...     def x(self):
    ...         print('Big computation...')
    ...         return 6 * 7
    >>> a = Example()
    >>> a.x
    Big computation...
    42
    >>> a.x
    42
    >>> a.delete_cache()
    >>> a.x
    Big computation...
    42
    """

    # noinspection PyAttributeOutsideInit
    def delete_cache(self) -> None:
        self._cached_properties = dict()


def parse_weak_order(s: str) -> list:
    """
    Convert a string representing a weak order to a list of sets.

    :param s: a string.
    :return: a list of sets, where each set is an indifference class. The first set of the list contains the top
        (= most liked) candidates, while the last set of the list contains the bottom (= most disliked) candidates.

    >>> s = 'Alice ~ Bob ~ Catherine32 > me > you ~ us > them'
    >>> parse_weak_order(s) == [{'Alice', 'Bob', 'Catherine32'}, {'me'}, {'you', 'us'}, {'them'}]
    True
    """

    # Build the parser
    candidate = Word(alphas.upper() + alphas.lower() + nums + '_')
    equiv_class = Group(candidate + ZeroOrMore(Word('~').suppress() + candidate))
    weak_preference = equiv_class + ZeroOrMore(Word('>').suppress() + equiv_class)
    empty_preference = ZeroOrMore(' ')

    # if s = 'Jean ~ Titi ~ tata32 > me > you ~ us > them', then
    # parsed = [['Jean', 'Titi', 'tata32'], ['me'], ['you', 'us'], ['them']]
    try:
        parsed = empty_preference.parseString(s, parseAll=True).asList()
    except ParseException:
        parsed = weak_preference.parseString(s, parseAll=True).asList()

    # Final conversion to format [{'Jean', 'tata32', 'Titi'}, {'me'}, {'us', 'you'}, {'them'}]
    return [NiceSet(s) for s in parsed]


def set_to_list(s: set) -> list:
    """
    Convert a set to a list.

    :param s: a set.
    :return: a list. The result is similar to list(s), but if the elements of the set are comparable, they appear in
        ascending order.

    >>> set_to_list({2, 42, 12})
    [2, 12, 42]
    """
    try:
        return sorted(s)
    except TypeError:
        return list(s)


def set_to_str(s: set) -> str:
    """
    Convert a set to a string.

    :param s: a set.
    :return: a string. The result is similar to str(s), but if the elements of the set are comparable, they appear in
        ascending order.

    >>> set_to_str({2, 42, 12})
    '{2, 12, 42}'
    """
    try:
        return '{' + str(sorted(s))[1:-1] + '}'
    except TypeError:
        return str(s)


class NiceSet(set):
    """
    A set that prints in order (when the elements are comparable).

    >>> my_set = NiceSet({'b', 'a', 'c'})
    >>> my_set
    {'a', 'b', 'c'}
    """

    def __repr__(self):
        try:
            return '{' + str(sorted(self))[1:-1] + '}'
        except TypeError:
            return str(set(self))


def dict_to_items(d: dict) -> list:
    """
    Convert a dict to a list of pairs (key, value).

    :param d: a dictionary.
    :return: a list of pairs. The result is similar to d.items(), but if the keys are comparable, they appear in
        ascending order.

    >>> dict_to_items({'b': 2, 'c': 0, 'a': 1})
    [('a', 1), ('b', 2), ('c', 0)]
    """
    try:
        return [(k, d[k]) for k in sorted(d.keys())]
    except TypeError:
        return list(d.items())


def dict_to_str(d: dict) -> str:
    """
    Convert dict to string.

    :param d: a dictionary.
    :return: a string. The result is similar to str(d), but if the keys are comparable, they appear in ascending order.

    >>> dict_to_str({'b': 2, 'c': 0, 'a': 1})
    "{'a': 1, 'b': 2, 'c': 0}"
    """
    try:
        return '{' + ', '.join(['%r: %r' % (k, d[k]) for k in sorted(d.keys())]) + '}'
    except TypeError:
        return str(d)


class NiceDict(dict):
    """
    A dict that prints in the order of the keys (when they are comparable).

    >>> my_dict = NiceDict({'b': 51, 'a': 42, 'c': 12})
    >>> my_dict
    {'a': 42, 'b': 51, 'c': 12}
    """

    def __repr__(self) -> str:
        return dict_to_str(self)


def take_closest(my_list, my_number):
    """
    In a list, take the closest element to a given number.

    :param my_list: a list sorted in ascending order.
    :param my_number: a number.
    :return: the element of ``my_list`` that is closest to ``my_number``. If two numbers are equally close, return the
        smallest number.

    >>> take_closest([0, 5, 10], 3)
    5

    From https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value .
    """
    pos = bisect_left(my_list, my_number)
    if pos == 0:
        return my_list[0]
    if pos == len(my_list):
        return my_list[-1]
    before = my_list[pos - 1]
    after = my_list[pos]
    if after - my_number < my_number - before:
        return after
    else:
        return before


def convert_number(x: Number):
    """
    Try to convert a number to a fraction (or an integer).

    :param x: a number.
    :return: ``x``, trying to convert it into a fraction (or an integer).

    >>> convert_number(2.5)
    Fraction(5, 2)
    >>> convert_number(2.0)
    2
    """
    if isinstance(x, float):
        x = str(x)
    try:
        value = Fraction(x)
        if value.denominator == 1:
            return value.numerator
        else:
            return value
    except (TypeError, ValueError):
        return x


def my_division(x: Number, y: Number, divide_by_zero: Number = None):
    """
    Division of two numbers, trying to be exact if it is reasonable.

    :param x: a number.
    :param y: a number.
    :param divide_by_zero: the value to be returned in case of division by zero. If None (default), then it raises
        a ZeroDivisionError.
    :return: the division of `x` by `y`.

    >>> my_division(5, 2)
    Fraction(5, 2)

    If `x` or `y` is a float, then the result is a float:

    >>> my_division(Fraction(5, 2), 0.1)
    25.0
    >>> my_division(0.1, Fraction(5, 2))
    0.04

    If `x` and `y` are integers, decimals or fractions, then the result is a fraction:

    >>> my_division(2, Fraction(5, 2))
    Fraction(4, 5)
    >>> my_division(Decimal('0.1'), Fraction(5, 2))
    Fraction(1, 25)

    You can specify a particular return value in case of division by zero:

    >>> my_division(1, 0, divide_by_zero=42)
    42
    """
    if y == 0:
        if divide_by_zero is None:
            raise ZeroDivisionError
        return divide_by_zero
    if isinstance(x, float) or isinstance(y, float):
        return x / y
    try:
        return convert_number(Fraction(x) / Fraction(y))
    except TypeError:
        raise NotImplementedError
