from whalrus import RuleBorda
from fractions import Fraction

def test():
   
    rule = RuleBorda(['a ~ b > c', 'b > c > a'])

    assert rule.gross_scores_ == {'a': Fraction(3, 2), 'b': Fraction(7, 2), 'c': 1}
    assert rule.scores_ == {'a': Fraction(3, 4), 'b': Fraction(7, 4), 'c': Fraction(1, 2)}

if __name__ == '__main__':
    test()