from whalrus.rules.rule_nanson import RuleNanson
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.priorities.priority import Priority

def test():

    rule = RuleNanson(['a > b > c > d', 'a > b > d > c'])
    assert rule.eliminations_[0].rule_.gross_scores_ == {'a': 6, 'b': 4, 'c': 1, 'd': 1}
    assert rule.eliminations_[1].rule_.gross_scores_ =={'a': 2, 'b': 0}
    assert rule.eliminations_[2].rule_.gross_scores_ == {'a': 0}
    assert rule.winner_ == 'a'

if __name__ == '__main__':
    test()

    