from whalrus import RuleRangeVoting, ConverterBallotToGrades, ScaleRange, BallotLevels, ScorerLevels
from fractions import Fraction

def test():

    rule = RuleRangeVoting([{'a': 1, 'b': .8, 'c': .2}, {'a': 0, 'b': .6, 'c': 1}])
    assert rule.scores_ == {'a': Fraction(1, 2), 'b': Fraction(7, 10), 'c': Fraction(3, 5)}
    rule = RuleRangeVoting([{'a': 10, 'b': 8, 'c': 2}, {'a': 0, 'b': 6, 'c': 10}])
    assert rule.scores_ == {'a': 5, 'b': 7, 'c': 6}


    assert RuleRangeVoting(['a > b > c']).profile_converted_[0].as_dict == {'a': 1, 'b': Fraction(1, 2), 'c': 0}
    assert RuleRangeVoting(
             ['a > b > c'], converter=ConverterBallotToGrades(scale=ScaleRange(0, 10))
         ).profile_converted_[0].as_dict == {'a': 10, 'b': 5, 'c': 0}

 

    b1 = BallotLevels({'a': 8, 'b': 10}, candidates={'a', 'b'})
    b2 = BallotLevels({'a': 6, 'c': 10}, candidates={'a', 'b', 'c'})

    assert RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'}).scores_ == {'a': 7, 'b': 10, 'c': 10, 'd': 0}
    assert RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'}, default_average=5).scores_ == {'a': 7, 'b': 10, 'c': 10, 'd': 5}
    assert RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'},
             scorer=ScorerLevels(level_ungraded=0)).scores_ == {'a': 7, 'b': 5, 'c': 10, 'd': 0}
    assert RuleRangeVoting([b1, b2], candidates={'a', 'b', 'c', 'd'},
             scorer=ScorerLevels(level_ungraded=0, level_absent=0)).scores_ ==  {'a': 7, 'b': 5, 'c': 5, 'd': 0}

if __name__ == '__main__':
    test()