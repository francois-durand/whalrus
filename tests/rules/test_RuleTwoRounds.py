from whalrus import RuleTwoRound, RuleBorda, EliminationLast

def test():
    rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'],
                      weights=[2, 2, 1])
    assert rule.first_round_.rule_.gross_scores_ =={'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 0}
    assert rule.second_round_.gross_scores_ == {'a': 3, 'b': 2}

    rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'],
                           weights=[2, 2, 1], rule1=RuleBorda())
    assert rule.first_round_.rule_.gross_scores_ == {'a': 17, 'b': 16, 'c': 12, 'd': 5, 'e': 0}
    assert rule.second_round_.gross_scores_ == {'a': 3, 'b': 2}

    rule = RuleTwoRound(['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'],
                             weights=[2, 2, 1], elimination=EliminationLast(k=-3))
    assert rule.first_round_.rule_.gross_scores_ == {'a': 2, 'b': 2, 'c': 1, 'd': 0, 'e': 0}
    assert rule.second_round_.gross_scores_ == {'a': 2, 'b': 2, 'c': 1}
    
if __name__ == '__main__':
    test()