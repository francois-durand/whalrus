import numpy as np 
from whalrus import RuleBucklinByRounds
from fractions import Fraction

def test():

    rule = RuleBucklinByRounds(['a > b > c > d', 'b > a > c > d',
                           'c > a > b > d', 'd > a > b > c'])

    assert rule.detailed_scores_[0] == {'a': Fraction(1, 4), 'b': Fraction(1, 4), 'c': Fraction(1, 4), 'd': Fraction(1, 4)}

    assert rule.detailed_scores_[1] ==  {'a': 1, 'b': Fraction(1, 2), 'c': Fraction(1, 4), 'd': Fraction(1, 4)}
    assert rule.n_rounds_ == 2

    assert rule.scores_ ==  {'a': 1, 'b': Fraction(1, 2), 'c': Fraction(1, 4), 'd': Fraction(1, 4)}
    assert rule.winner_ == 'a'

if __name__ == '__main__':
    test()