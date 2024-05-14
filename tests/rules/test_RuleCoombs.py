from whalrus import RuleCoombs
from fractions import Fraction
import numpy as np

def test():

    rule = RuleCoombs(['a > b > c', 'b > a > c', 'c > a > b'], weights=[2, 3, 4])
    assert rule.eliminations_[0].rule_.gross_scores_ == {'a': 0, 'b': -4, 'c': -5}
    assert rule.eliminations_[1].rule_.gross_scores_ == {'a': -3, 'b': -6}
    assert rule.eliminations_[2].rule_.gross_scores_ == {'a': -9}
    assert rule.winner_ == 'a'

if __name__ == '__main__':
    test()