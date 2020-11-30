from whalrus import RuleMajorityJudgment, ScaleRange


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
    pass


def test_same_score():
    """
        >>> rule = RuleMajorityJudgment()
        >>> rule.compare_scores((2, 0.4, 0.3), (2, 0.4, 0.3))
        0
    """
    pass


def test_compare():
    """
        >>> rule = RuleMajorityJudgment()
        >>> rule.compare_scores((2, 0.4, -0.2), (2, 0.4, -0.3))
        1
    """
    pass
