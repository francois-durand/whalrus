from whalrus.rules.rule_nanson import RuleNanson
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.priorities.priority import Priority

def test():

    rule = RuleNanson(['a > b > c > d', 'a > b > d > c'], weights = [2,1])
    assert rule.eliminations_[0].rule_.gross_scores_ == {'a': 9, 'b': 6, 'c': 2, 'd': 1}
    assert rule.eliminations_[1].rule_.gross_scores_ =={'a': 3, 'b': 0}
    assert rule.eliminations_[2].rule_.gross_scores_ == {'a': 0}
    assert rule.winner_ == 'a'

if __name__ == '__main__':
    test()

    