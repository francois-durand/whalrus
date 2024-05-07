from whalrus import RuleKBest, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax


def test():
    rule = RuleKBest(ballots = ['a', 'b', 'c', 'd', 'e'], weights = [4, 3, 3, 3, 2],
                     committee_size = 2, base_rule = RulePlurality(tie_break=Priority.ASCENDING))                 
    assert rule.winning_committee_ == {'a', 'b'}
    assert rule.cowinning_committees_ == {frozenset({'a', 'b'})}
    assert rule.trailing_committee_ == {'d', 'e'}
    assert rule.cotrailing_committees_ == {frozenset({'d', 'e'})}

    rule = RuleKBest(ballots = ['a', 'b', 'c', 'd', 'e'], weights = [4, 3, 3, 3, 2],
                     committee_size = 2, base_rule = RulePlurality(),
                     use_base_rule_tie_break=False, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    
    assert rule.winning_committee_ == {'a', 'b'}
    assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a', 'c'}), frozenset({'a', 'd'})}
    print(rule.trailing_committee_)
    assert rule.trailing_committee_ == {'d', 'e'}
    assert rule.cotrailing_committees_ == {frozenset({'b', 'e'}), frozenset({'c', 'e'}), frozenset({'d', 'e'})}

if __name__ == '__main__': 
    test()  