from whalrus import RuleChamberlinCourant, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax



def test():

    rule = RuleChamberlinCourant(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    assert rule.winning_committee_ == {'a', 'd'}
    #assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a','c'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    #assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c','d'})}

    rule = RuleChamberlinCourant(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
                          committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    assert rule.winning_committee_ == {'a', 'b'}
    assert rule.cowinning_committees_ == {frozenset({'a', 'b'}), frozenset({'a', 'c'}), frozenset({'a', 'd'})}
    assert rule.trailing_committee_ == {'c', 'd'}
    assert rule.cotrailing_committees_ == {frozenset({'b', 'd'}), frozenset({'c', 'd'})}

#      >>> cc.winning_committee_
#     {'a', 'd'}
#     >>> cc.trailing_committee_
#     {'c', 'd'}

#    >>> cc.cowinning_committees_
#     {{'a', 'b'}, {'a', 'c'}, {'a', 'd'}}
#     >>> cc.winning_committee_
#     {'a', 'b'}
#     >>> cc.cotrailing_committees_
#     {{'b', 'd'}, {'c', 'd'}}
#     >>> cc.trailing_committee_
#     {'c', 'd'}

if __name__ == '__main__':
    test()