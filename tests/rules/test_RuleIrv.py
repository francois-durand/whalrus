from whalrus import RuleIRV
from whalrus.priorities.priority import Priority

def test():

    rule = RuleIRV(['a > b > c', 'b > a > c', 'c > a > b'], weights=[2, 3, 4])
    assert rule.eliminations_[0].rule_.gross_scores_ == {'a': 2, 'b': 3, 'c': 4}
    assert rule.eliminations_[1].rule_.gross_scores_ == {'b': 5, 'c': 4}
    assert rule.eliminations_[2].rule_.gross_scores_ == {'b': 9}
    assert rule.winner_ == 'b'

    rule = RuleIRV(['a > c > b', 'b > a > c', 'c > a > b'], weights=[1, 2, 1],
              tie_break=Priority.ASCENDING)
    assert rule.eliminations_[0].rule_.gross_scores_ == {'a': 1, 'b': 2, 'c': 1}
    assert rule.eliminations_[1].rule_.gross_scores_ == {'a': 2, 'b': 2}
    assert rule.eliminations_[2].rule_.gross_scores_ == {'a': 4}
    assert rule.winner_ == 'a'

if __name__ == '__main__':
    test()
