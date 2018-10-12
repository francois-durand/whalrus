from whalrus.rule.RuleSequentialElimination import RuleSequentialElimination
from whalrus.rule.RulePlurality import RulePlurality
from whalrus.priority.Priority import Priority


def test():
    irv = RuleSequentialElimination(base_rule=RulePlurality())
    irv([
        'a > b > c',
        'b > a > c',
        'c > a > b'
    ], weights=[2, 3, 4])
    assert irv.order_ == [{'b'}, {'c'}, {'a'}]
    assert irv.winner_ == 'b'

    irv = RuleSequentialElimination(base_rule=RulePlurality(tie_break=Priority.ASCENDING))
    irv([
        'a > b > c > d',
        'd > b > c > a',
        'b > a > c > d',
        'c > a > b > d'
    ], weights=[1, 1, 3, 4])
    assert irv.order_ == [{'b'}, {'c'}, {'a'}, {'d'}]
    assert irv.winner_ == 'b'
