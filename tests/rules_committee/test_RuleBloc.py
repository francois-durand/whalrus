from whalrus import RuleBloc, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax
import profile_Examples_c



def test():

    rule = RuleBloc(['a > b > c > d', 'd > b > a > c', 'a > c > b > d'], committee_size=2)

    
    
    assert rule.winning_committee_ == {'a', 'b'}
    #assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a','c'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    #assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c','d'})}

    rule = RuleBloc(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
                          committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    assert rule.winning_committee_ == {'a', 'b'}
    assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a', 'c'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c', 'd'})}


    rule = RuleBloc(profile_Examples_c.p1, committee_size = profile_Examples_c.k1)
    
    assert rule.cowinning_committees_ == {frozenset({'b','e'}),frozenset({'b','f'})}
