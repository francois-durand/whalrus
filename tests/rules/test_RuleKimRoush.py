from whalrus.rules.rule_kim_roush import RuleKimRoush
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.priorities.priority import Priority

def test():

    rule = RuleKimRoush(['a > b > c > d', 'a > b > d > c'])
    assert rule.eliminations_[0].rule_.gross_scores_ == {'a': 0, 'b': 0, 'c': -1, 'd': -1}
    assert rule.eliminations_[1].rule_.gross_scores_ == {'a': 0, 'b': -2}
    assert rule.eliminations_[2].rule_.gross_scores_ == {'a': -2}
    assert rule.winner_ == 'a'

if __name__ == '__main__':
    test()