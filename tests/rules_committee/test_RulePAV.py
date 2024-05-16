from whalrus import RulePAV, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax
import profile_Examples


def test():
    rule = RulePAV([{'a': 1, 'b': 1, 'c': 0, 'd': 0}, {'d': 1, 'b': 1, 'a': 1, 'c': 0}, {'a': 1, 'b': 0, 'c': 0, 'd': 0}], committee_size=2)               
    assert rule.winning_committee_ == {'a', 'b'}
    #assert rule.cowinning_committees_ == {frozenset({'a', 'b'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    #assert rule.cotrailing_committees_ == {frozenset({'d', 'e'})}

    rule = RulePAV([{'a': 1, 'b': 1, 'c': 0, 'd': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0}],
                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    
    assert rule.winning_committee_ == {'a', 'b'}
    assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a', 'c'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c', 'd'})}

    rule = RulePAV(profile_Examples.p2, committee_size=2)
    print(rule.winning_committee_)

if __name__ == '__main__': 
    test()  


