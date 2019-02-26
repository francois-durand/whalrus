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
from whalrus import BallotLevels
from whalrus import ScaleFromList


def test():
    ballot = BallotLevels({'a': 'Good', 'b': 'Bad', 'c': 'Bad'}, scale=ScaleFromList(['Bad', 'Medium', 'Good']))
    assert ballot.as_dict == {'a': 'Good', 'b': 'Bad', 'c': 'Bad'}
    assert ballot.as_weak_order == [{'a'}, {'b', 'c'}]
    assert ballot.candidates_in_b == {'a', 'b', 'c'}
    assert ballot.candidates == {'a', 'b', 'c'}
    assert ballot.candidates_not_in_b == set()
    assert len(ballot) == 3
    assert 'a' in ballot
    # noinspection PyUnresolvedReferences
    assert ballot.scale.levels == ['Bad', 'Medium', 'Good']
    assert repr(ballot) == "BallotLevels({'a': 'Good', 'b': 'Bad', 'c': 'Bad'}, candidates={'a', 'b', 'c'}, " \
                           "scale=ScaleFromList(levels=['Bad', 'Medium', 'Good']))"
    assert str(ballot) == 'a: Good, b: Bad, c: Bad'
    assert ballot['a'] == 'Good'
    assert 'a' in ballot.keys()
    assert 'Good' in ballot.values()
    assert ('a', 'Good') in ballot.items()


def test_inferred_scale():
    assert repr(BallotLevels({'a': 10, 'b': 7, 'c': 0}).scale) == 'Scale()'
    assert repr(BallotLevels({'a': 10, 'b': 7., 'c': 0}).scale) == 'Scale()'
    assert repr(BallotLevels({'a': 'B', 'b': 'C', 'c': 'A'}).scale) == 'Scale()'


def test_empty_ballot():
    ballot = BallotLevels({}, candidates={'a', 'b', 'c'})
    assert ballot.as_dict == {}
    assert repr(ballot.scale) == 'Scale()'
