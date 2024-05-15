from whalrus import RuleMajorityJudgment, ScaleRange, ScaleFromList, ScorerBorda, ConverterBallotToOrder


def test_default_median():
    """
        >>> rule = RuleMajorityJudgment(scale=ScaleRange(0, 1), default_median=0.1)
        >>> rule([{'a': 1, 'b': 0}], candidates={'a', 'b', 'c'}).scores_
        {'a': (1, 0, 0), 'b': (0, 0, 0), 'c': (0.1, 0, 0)}
        >>> rule.worst_score_
        (0, 0, 0)
        >>> rule.order_
        [{'a'}, {'c'}, {'b'}]
    """
    rule = RuleMajorityJudgment(scale=ScaleRange(0, 1), default_median=0.1)
    assert rule([{'a': 1, 'b': 0}], candidates={'a', 'b', 'c'}).scores_ == {'a': (1, 0, 0), 'b': (0, 0, 0), 'c': (0.1, 0, 0)}
    assert rule.worst_score_ ==  (0, 0, 0)
    assert rule.order_ == [{'a'}, {'c'}, {'b'}]

def test_same_score():
    """
        >>> rule = RuleMajorityJudgment()
        >>> rule.compare_scores((2, 0.4, 0.3), (2, 0.4, 0.3))
        0
    """
    rule = RuleMajorityJudgment()
    assert rule.compare_scores((2, 0.4, 0.3), (2, 0.4, 0.3)) == 0


def test_compare():
    """
        >>> rule = RuleMajorityJudgment()
        >>> rule.compare_scores((2, 0.4, -0.2), (2, 0.4, -0.3))
        1
    """
    rule = RuleMajorityJudgment()
    assert rule.compare_scores((2, 0.4, -0.2), (2, 0.4, -0.3)) == 1

def test():
    
    rule = RuleMajorityJudgment([{'a': 1, 'b': 1}, {'a': .5, 'b': .6},
                                      {'a': .5, 'b': .4}, {'a': .3, 'b': .2}])
    assert rule.scores_as_floats_ =={'a': (0.5, -0.25, 0.25), 'b': (0.4, 0.5, -0.25)}
    assert rule.winner_ == 'a'

    rule = RuleMajorityJudgment([
            {'a': 'Excellent', 'b': 'Excellent'}, {'a': 'Good', 'b': 'Very Good'},
            {'a': 'Good', 'b': 'Acceptable'}, {'a': 'Poor', 'b': 'To Reject'}
        ], scale=ScaleFromList(['To Reject', 'Poor', 'Acceptable', 'Good', 'Very Good', 'Excellent']))
    assert  rule.scores_as_floats_ == {'a': ('Good', -0.25, 0.25), 'b': ('Acceptable', 0.5, -0.25)}
    assert  rule.winner_ == 'a'



    rule = RuleMajorityJudgment(scorer=ScorerBorda(), converter=ConverterBallotToOrder())
    assert  rule(['a > b ~ c > d', 'c > a > b > d']).scores_as_floats_ == {'a': (2.0, 0.5, 0.0), 'b': (1.0, 0.5, 0.0), 'c': (1.5, 0.5, 0.0), 'd': (0.0, 0.0, 0.0)}
    assert  rule.winner_ == 'a'


if __name__ == '__main__':
    test()
    test_compare()
    test_default_median()
    test_same_score()