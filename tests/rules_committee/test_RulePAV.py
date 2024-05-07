from whalrus import RulePAV, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax


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

    #  >>> cc = RulePAV([{'a': 1, 'b': 1, 'c': 0, 'd': 0}, {'d': 1, 'b': 1, 'a': 1, 'c': 0}, {'a': 1, 'b': 0, 'c': 0, 'd': 0}], committee_size=2)
    # >>> cc.scores_
    # {{'a', 'b'}: 4.0, {'a', 'c'}: 3.0, {'a', 'd'}: 3.5, {'b', 'c'}: 2.0, {'b', 'd'}: 2.5, {'c', 'd'}: 1.0
    # >>> cc.winning_committee_
    # {'a', 'b'}
    # >>> cc.trailing_committee_
    # {'c', 'd'}

    # >>> cc = RulePAV([{'a': 1, 'b': 1, 'c': 0, 'd': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 0}, {'a': 1, 'b': 0, 'c': 1, 'd': 0}, {'a': 1, 'b': 1, 'c': 0, 'd': 0}],
    # ...                             committee_size=2, tie_break=PriorityLiftedLeximax(Priority.ASCENDING))
    # >>> cc.scores_
    # {{'a', 'b'}: 5.0, {'a', 'c'}: 5.0, {'a', 'd'}: 4.0, {'b', 'c'}: 4.0, {'b', 'd'}: 2.0, {'c', 'd'}: 2.0}
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


