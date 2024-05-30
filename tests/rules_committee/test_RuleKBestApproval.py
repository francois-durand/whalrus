from whalrus import RuleKBestApproval, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax
import profile_Examples_c


def test():
    rule = RuleKBestApproval([{'a': 1, 'b': 1, 'c': 0, 'd': 0}, {'d': 1, 'b': 1, 'a': 1, 'c': 0}, {'a': 1, 'b': 0, 'c': 0, 'd': 0}], committee_size=2)               

    assert rule.winning_committee_ == {'a', 'b'}
    #assert rule.cowinning_committees_ == {frozenset({'a', 'b'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    #assert rule.cotrailing_committees_ == {frozenset({'d', 'e'})}

    rule = RuleKBestApproval([{'a': 1, 'b': 1, 'c': 0, 'd': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0}],
                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    
    assert rule.winning_committee_ == {'a', 'b'}
    assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a', 'c'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c', 'd'})}

    rule = RuleKBestApproval(profile_Examples_c.p_a2, committee_size=2)
