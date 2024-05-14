import numpy as np
from whalrus import RuleBlack
from fractions import Fraction

def test_condorcet():

    rule = RuleBlack(ballots=['a > b > c', 'b > c > a'], weights=[3, 2])
    np.testing.assert_array_equal(rule.rule_condorcet_.matrix_majority_.as_array_,
            np.array([[Fraction(1, 2), 1, 1],
                   [0, Fraction(1, 2), 1],
                   [0, 0, Fraction(1, 2)]], dtype=object))
    
    np.testing.assert_array_equal(rule.rule_condorcet_.matrix_majority_.matrix_weighted_majority_.as_array_,
        np.array([[0, Fraction(3, 5), Fraction(3, 5)],
               [Fraction(2, 5), 0, 1],
               [Fraction(2, 5), 0, 0]], dtype=object))
    assert rule.order_ == [{'a'}, {'b'}, {'c'}]

    rule = RuleBlack(ballots=['a > b > c', 'b > c > a', 'c > a > b'], weights=[3, 2, 2])
    np.testing.assert_array_equal(rule.rule_condorcet_.matrix_majority_.matrix_weighted_majority_.as_array_,
        np.array([[0, Fraction(5, 7), Fraction(3, 7)],
               [Fraction(2, 7), 0, Fraction(5, 7)],
               [Fraction(4, 7), Fraction(2, 7), 0]], dtype=object))
    assert rule.order_ == [{'a'}, {'b'}, {'c'}]

def test_borda():
    rule = RuleBlack(ballots=['a > b > c', 'b > c > a'], weights=[3, 2])
    assert rule.rule_borda_.scores_ == {'a': Fraction(6, 5), 'b': Fraction(7, 5), 'c': Fraction(2, 5)}

if __name__ == '__main__':
    test_borda()
    test_condorcet()