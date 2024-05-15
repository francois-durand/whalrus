from whalrus import RuleKBestBorda, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax
import profile_Examples



def test():

    rule = RuleKBestBorda(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    assert rule.winning_committee_ == {'a', 'b'}
    #assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a','c'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    #assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c','d'})}

    rule = RuleKBestBorda(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
                          committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    assert rule.winning_committee_ == {'a', 'b'}
    assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a', 'c'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c', 'd'})}

  

    rule = RuleKBestBorda(profile_Examples.p1, committee_size = profile_Examples.k1)
    assert rule.cowinning_committees_ == {frozenset({'b','c'}), frozenset({'b', 'd'})}

if __name__ == '__main__':
    test()