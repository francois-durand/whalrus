from whalrus import RuleBloc, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax
import profile_Examples



def test():

    rule = RuleBloc(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)

    
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

    # cc.cowinning_committees_
    # {{'a', 'b'}, {'a', 'c'}}
    # >>> cc.winning_committee_
    # {'a', 'b'}
    # >>> cc.cotrailing_committees_
    # {{'b', 'd'}, {'c', 'd'}}
    # >>> cc.trailing_committee_
    # {'c', 'd'}

    rule = RuleBloc(profile_Examples.p1, committee_size = profile_Examples.k1)
    print(rule.scores_)
    assert rule.cowinning_committees_ == {frozenset({'b','e'}),frozenset({'b','f'})}

if __name__ == '__main__':
    test()