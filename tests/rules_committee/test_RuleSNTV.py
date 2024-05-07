from whalrus import RuleSNTV, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax

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


    # >>> cc = RuleSNTV(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    # >>> cc.scores_
    # {{'a', 'b'}: 2, {'a', 'c'}: 2, {'a', 'd'}: 3, {'b', 'c'}: 0, {'b', 'd'}: 1, {'c', 'd'}: 1}
    # >>> cc.winning_committee_
    # {'a', 'd'}
    # >>> cc.trailing_committee_
    # {'b', 'c'}

    # >>> cc = RuleSNTV(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
    # ...                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    # >>> cc.scores_
    # {{'a', 'b'}: 4, {'a', 'c'}: 4, {'a', 'd'}: 4, {'b', 'c'}: 0, {'b', 'd'}: 0, {'c', 'd'}: 0}
    # >>> cc.cowinning_committees_
    # {{'a', 'b'}, {'a', 'c'}, {'a', 'd'}}
    # >>> cc.winning_committee_
    # {'a', 'b'}
    # >>> cc.cotrailing_committees_
    # {{'b', 'c'}, {'b', 'd'}, {'c', 'd'}}
    # >>> cc.trailing_committee_
    # {'c', 'd'}

if __name__ == '__main__':
    test()
