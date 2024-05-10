from whalrus import RuleKBestBorda, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax



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

    #  >>> cc = RuleKBestBorda(['a > b > c > d', 'd > b > a > c', 'a > b > c > d'], committee_size=2)
    # >>> cc.scores_
    # {{'a', 'b'}: 13, {'a', 'c'}: 9, {'a', 'd'}: 10, {'b', 'c'}: 8, {'b', 'd'}: 9, {'c', 'd'}: 5}
    # >>> cc.winning_committee_
    # {'a', 'b'}
    # >>> cc.trailing_committee_
    # {'c', 'd'}

    # >>> cc = RuleKBestBorda(['a > b > c > d', 'a > c > b > d', 'a > c > b > d', 'a > b > c > d'],
    # ...                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    # >>> cc.scores_
    # {{'a', 'b'}: 18, {'a', 'c'}: 18, {'a', 'd'}: 12, {'b', 'c'}: 12, {'b', 'd'}: 6, {'c', 'd'}: 6}
    # >>> cc.cowinning_committees_
    # {{'a', 'b'}, {'a', 'c'}}
    # >>> cc.winning_committee_
    # {'a', 'b'}
    # >>> cc.cotrailing_committees_
    # {{'b', 'd'}, {'c', 'd'}}
    # >>> cc.trailing_committee_
    # {'c', 'd'}

if __name__ == '__main__':
    test()