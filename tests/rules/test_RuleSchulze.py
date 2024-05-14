from fractions import Fraction
from whalrus import RuleSchulze
import numpy as np

def test():

    rule = RuleSchulze(['a > b > c', 'b > c > a', 'c > a > b'], weights=[4, 3, 2])
    np.testing.assert_array_equal(rule.matrix_schulze_.as_array_,
        np.array([[0, Fraction(2, 3), Fraction(2, 3)],
               [Fraction(5, 9), 0, Fraction(7, 9)],
               [Fraction(5, 9), Fraction(5, 9), 0]], dtype=object))
    assert rule.winner_ == 'a'

if __name__ == "__main__":
    test()


