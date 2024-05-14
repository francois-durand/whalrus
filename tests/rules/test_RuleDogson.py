from whalrus import RuleSimplifiedDodgson
from fractions import Fraction
import numpy as np

def test():

    rule = RuleSimplifiedDodgson(ballots=['a > b > c', 'b > a > c', 'c > a > b'],
                                     weights=[3, 3, 2])
    np.testing.assert_array_equal(rule.matrix_weighted_majority_.as_array_,
        np.array([[0, Fraction(1, 4), Fraction(1, 2)],
               [Fraction(-1, 4), 0, Fraction(1, 2)],
               [Fraction(-1, 2), Fraction(-1, 2), 0]], dtype=object))
    assert rule.scores_ == {'a': 0, 'b': Fraction(-1, 4), 'c': -1}
    assert rule.winner_ == 'a'
    
if __name__ == '__main__':
    test()