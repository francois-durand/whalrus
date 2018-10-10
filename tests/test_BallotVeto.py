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
from whalrus import BallotVeto
from whalrus import Priority


def test():
    ballot = BallotVeto('a', candidates={'a', 'b', 'c'})
    assert ballot.last() == 'a'
    with pytest.raises(ValueError):
        _ = ballot.first()
    assert ballot.first(priority=Priority.ASCENDING) == 'b'
    assert ballot.first(priority=Priority.DESCENDING) == 'c'
    assert ballot.first(priority=Priority.RANDOM) in {'b', 'c'}

    assert BallotVeto('a', candidates={'a', 'b'}).first() == 'b'


def test_empty_ballot():
    ballot = BallotVeto(None, candidates={'a', 'b', 'c'})
    assert ballot.first() is None
    assert ballot.last() is None
