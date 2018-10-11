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
import pytest
from pyparsing import ParseException
from whalrus import BallotOrder
from whalrus import Priority


def test_create_ballot():
    # Different kinds of syntax for the input ballot
    assert repr(BallotOrder([{'A', 'B'}, {'C'}])) == \
        "BallotOrder([{'A', 'B'}, 'C'], candidates={'A', 'B', 'C'})"
    assert repr(BallotOrder([{'A', 'B'}, 'C'])) == \
        "BallotOrder([{'A', 'B'}, 'C'], candidates={'A', 'B', 'C'})"
    assert repr(BallotOrder(({'A', 'B'}, {'C'}))) == \
        "BallotOrder([{'A', 'B'}, 'C'], candidates={'A', 'B', 'C'})"
    assert repr(BallotOrder(({'A', 'B'}, 'C'))) == \
        "BallotOrder([{'A', 'B'}, 'C'], candidates={'A', 'B', 'C'})"

    with pytest.raises(ParseException):
        # Try to parse the string, but fails.
        BallotOrder('A * B')

    with pytest.raises(TypeError):
        # This is not an accepted type.
        BallotOrder(42)

    # Different ways to enter an empty ballot
    assert repr(BallotOrder(())) == "BallotOrder([], candidates={})"
    assert repr(BallotOrder([])) == "BallotOrder([], candidates={})"
    assert repr(BallotOrder({})) == "BallotOrder([], candidates={})"
    assert repr(BallotOrder('')) == "BallotOrder([], candidates={})"


def test_empty_ballot():
    ballot = BallotOrder('', candidates={'a', 'b', 'c'})
    assert repr(ballot) == "BallotOrder([], candidates={'a', 'b', 'c'})"
    assert str(ballot) == '(unordered: a, b, c)'
    assert ballot.as_weak_order == []
    assert ballot.candidates_in_b == set()
    assert ballot.candidates == {'a', 'b', 'c'}
    assert ballot.candidates_not_in_b == {'a', 'b', 'c'}
    assert len(ballot) == 0
    assert 'a' not in ballot
    with pytest.raises(ValueError):
        _ = ballot.first()
    with pytest.raises(ValueError):
        _ = ballot.last()
    assert ballot.is_strict
    assert ballot.as_strict_order == []


def test_ballot_mixed_types():
    class Candidate:
        def __init__(self, name, age):
            self.name = name
            self.age = age

        def __repr__(self):
            return 'Candidate(name=%r, age=%r)' % (self.name, self.age)

        def __str__(self):
            return self.name
    john = Candidate('John Doe', 42)
    jane = Candidate('Jane Doe', 51)
    ballot = BallotOrder([{0, 42}, (1, 2), john, 'a'], candidates={0, 42, (1, 2), john, 'a', jane})
    assert isinstance(repr(ballot), str)
    assert str(ballot) == "0 ~ 42 > (1, 2) > John Doe > a (unordered: Jane Doe)"
    assert ballot.as_weak_order == [{0, 42}, {(1, 2)}, {john}, {'a'}]
    assert ballot.candidates_in_b == {0, 42, (1, 2), john, 'a'}
    assert ballot.candidates == {0, 42, (1, 2), john, jane, 'a'}
    assert ballot.candidates_not_in_b == {jane}
    assert len(ballot) == 5
    assert john in ballot
    with pytest.raises(ValueError):
        _ = ballot.first()
    assert ballot.last() == jane
    assert ballot.first(priority=Priority.RANDOM) in {0, 42}
    assert ballot.last(include_unordered=True) == jane
    assert ballot.last(include_unordered=False) == 'a'
    assert not ballot.is_strict
    with pytest.raises(ValueError):
        _ = ballot.as_strict_order
