from whalrus import RuleCopeland
from whalrus import MatrixMajority
from fractions import Fraction
import numpy as np

def test():

    rule = RuleCopeland(ballots=['a > b > c', 'b > a > c', 'c > a > b'], matrix = MatrixMajority(equal=1))
    
    assert rule.scores_ == {'a': 2, 'b': 1, 'c': 0}
    np.testing.assert_array_equal(rule.matrix_majority_.as_array_, np.array([[Fraction(1, 2), 1, 1],
               [0, Fraction(1, 2), 1],
               [0, 0, Fraction(1, 2)]], dtype=object))

if __name__ == '__main__':
    test()
