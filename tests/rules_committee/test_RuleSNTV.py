from whalrus import RuleSNTV, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax
import profile_Examples_c

def test():

    rule = RuleSNTV(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    assert rule.winning_committee_ == {'a', 'd'}
    #assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a','c'})}
    assert rule.trailing_committee_ == {'b', 'c'}
    #assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c','d'})}

    rule = RuleSNTV(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
                          committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    assert rule.winning_committee_ == {'a', 'b'}
    assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a', 'c'}), frozenset({'a','d'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    assert rule.cotrailing_committees_ == {frozenset({'b', 'c'}), frozenset({'c', 'd'}), frozenset({'b','d'})}




    rule = RuleSNTV(profile_Examples_c.p1, committee_size = profile_Examples_c.k1)

    assert rule.winning_committee_ == {'a', 'f'}

