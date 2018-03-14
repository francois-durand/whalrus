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
from functools import lru_cache
from whalrus.voting_rules.ScoreRule import ScoreRule


class Plurality(ScoreRule):

    def load_profile(self, p):
        self.p = p
        self.ballots = {voter: ballot.to_plurality_ballot()
                        for voter, ballot in p}
        self.empty_lru_caches()

    @lru_cache(maxsize=1)
    def scores(self):
        _scores = dict()
        for voter, ballot in self.ballots:
            if ballot.candidate() in _scores.keys():
                _scores[ballot.candidate()] += 1
            else:
                _scores[ballot.candidate()] = 1
        return _scores
