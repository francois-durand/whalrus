from whalrus import RuleCondorcet
from whalrus import MatrixMajority
from fractions import Fraction
import numpy as np

def test():
   
    rule = RuleCondorcet(ballots=['a > b > c', 'b > a > c', 'c > a > b'])

    assert rule.order_ == [{'a'}, {'b', 'c'}]
    rule = RuleCondorcet(ballots=['a > b > c', 'b > c > a', 'c > a > b'])
    
    assert rule.order_ ==  [{'a', 'b', 'c'}]

    rule = RuleCondorcet(ballots=['a ~ b > c'], matrix_majority=MatrixMajority(equal=1))
   
    np.testing.assert_almost_equal(rule.matrix_majority_.as_array_, np.array([[Fraction(1, 2), 1, 1],
               [1, Fraction(1, 2), 1],
               [0, 0, Fraction(1, 2)]], dtype=object))
    assert rule.order_ == [{'a', 'b'}, {'c'}]

if __name__ == '__main__':
    test()