# -*- coding: utf-8 -*-
"""
Copyright Sylvain Bouveret, Yann Chevaleyre and François Durand
sylvain.bouveret@imag.fr, yann.chevaleyre@dauphine.fr, fradurand@gmail.com

This file is part of Whalrus.

    Whalrus is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Whalrus is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Whalrus.  If not, see <http://www.gnu.org/licenses/>.
"""
from pyparsing import Group, Word, ZeroOrMore, alphas, nums, ParseException


# noinspection PyPep8Naming
class cached_property:
    """
    Decorator used in replacement of @property to put the value in cache automatically.

    The first time the attribute is used, it is computed on-demand and put in cache. Later accesses to the
    attributes will use the cached value.

    Technically, this is a "descriptor".

    Adapted from https://stackoverflow.com/questions/4037481/caching-attributes-of-classes-in-python.

    Cf. :class:`DeleteCacheMixin` for an example.
    """

    def __init__(self, factory: callable):
        """
        This code runs when the decorator is applied to the function (i.e. when the function is defined).

        :meth:`factory` is the function.
        """
        self._factory = factory
        self._attr_name = factory.__name__

    def __get__(self, instance: object, owner: object) -> object:
        """
        This code runs only when the decorated function is directly called (which happens only when the value is not
        in cache).
        """
        # This hack is used so that the decorated function has the same docstring as the original function.
        if instance is None:
            def f():
                pass
            f.__doc__ = self._factory.__doc__
            property(f)
            return f
        # Compute the value.
        value = self._factory(instance)
        # Create the attribute and assign the value.
        # In the Python precedence order, the attribute "hides" the function of the same name.
        setattr(instance, self._attr_name, value)
        # Add the attribute name in the set cached_properties of the instance.
        try:
            instance.cached_properties.add(self._attr_name)
        except AttributeError:
            instance.cached_properties = {self._attr_name}
        # Return the value.
        return value


class DeleteCacheMixin:
    """
    Mixin used to delete cached properties.

    Cf. decorator :class:`cached_property`.

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
    def delete_cache(self) -> None:
        if not hasattr(self, 'cached_properties'):
            return
        for p in self.cached_properties:
            del self.__dict__[p]
        # noinspection PyAttributeOutsideInit
        self.cached_properties = set()


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

    # Final conversion to format [{'Jean', 'Titi', 'tata32'}, {'me'}, {'you', 'us'}, {'them'}]
    return [set(s) for s in parsed]


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
