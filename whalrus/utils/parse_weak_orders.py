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
from toolz import merge

def parse_weak_order(s):
    """
    Converts a string representing a weak-order to a dictionary
    Throws a 'ParseException' if the string is not a valid weak-order

    TODO: remove when obsolete

    Example:

    >>> s = 'Jean ~ Titi ~ tata32 > moi > toi ~ nous > eux'
    >>> parse_weak_order(s)
    {'Jean': 3, 'Titi': 3, 'tata32': 3, 'moi': 2, 'toi': 1, 'nous': 1, 'eux': 0}

    Another example.
    Here, an exception is thrown because the string is not a valid weak-order:

    >>> try:
    ...    parse_weak_order('a * b')
    ... except ParseException:
    ...    print('invalid')
    invalid

    """

    candidate = Word(alphas.upper() + alphas.lower() + nums + '_')
    equiv_class = Group(candidate + ZeroOrMore(Word('~').suppress() + candidate))
    weakpref = equiv_class + ZeroOrMore(Word('>').suppress() + equiv_class)

    # if s = 'Jean ~ Titi ~ tata32 > moi > toi ~ nous > eux', then
    # parsed = [['Jean', 'Titi', 'tata32'], ['moi'], ['toi', 'nous'], ['eux']]
    parsed = weakpref.parseString(s, parseAll=True).asList()

    lst = []
    for v, t in enumerate(reversed(parsed)):
        lst = [(c, v) for c in t] + lst

    return dict(lst)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

