from whalrus import RuleBaldwin
from fractions import Fraction

def test():
   
    rule = RuleBaldwin(['a > b > c', 'a > b ~ c'])

    assert rule.eliminations_[0].rule_.gross_scores_ == {'a': 4, 'b': Fraction(3, 2), 'c': Fraction(1, 2)}
    assert rule.eliminations_[1].rule_.gross_scores_ == {'a': 2, 'b': 0}
    assert rule.eliminations_[2].rule_.gross_scores_ == {'a': 0}
    assert rule.winner_ == 'a'

if __name__ == '__main__':
    test()