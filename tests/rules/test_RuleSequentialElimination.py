from whalrus import RuleSequentialElimination, RulePlurality, EliminationLast


def test_default_elimination():
    """
        >>> rule = RuleSequentialElimination(rules=[RulePlurality(), RulePlurality()])
        >>> rule.eliminations[0].k
        1
    """
    pass


def test_default_number_of_rounds():
    """
        >>> rule = RuleSequentialElimination(rules=RulePlurality())
        >>> len(rule.eliminations)
        0
    """
    pass


def test_order():
    """
        >>> rule = RuleSequentialElimination(
        ...     ['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'], weights=[2, 2, 1],
        ...     rules=RulePlurality(), eliminations=[EliminationLast(k=-2)])
        >>> rule.order_
        [{'a'}, {'b'}, {'c'}, {'d', 'e'}]
    """
    pass
