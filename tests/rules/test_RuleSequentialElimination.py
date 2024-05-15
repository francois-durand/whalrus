from whalrus import RuleSequentialElimination, RulePlurality, EliminationLast


def test_default_elimination():
    """
        >>> rule = RuleSequentialElimination(rules=[RulePlurality(), RulePlurality()])
        >>> rule.eliminations[0].k
        1
    """
    rule = RuleSequentialElimination(rules=[RulePlurality(), RulePlurality()])
    assert rule.eliminations[0].k == 1


def test_default_number_of_rounds():
    """
        >>> rule = RuleSequentialElimination(rules=RulePlurality())
        >>> len(rule.eliminations)
        0
    """
    rule = RuleSequentialElimination(rules=RulePlurality())
    assert len(rule.eliminations) == 0


def test_order():
    """
        >>> rule = RuleSequentialElimination(
        ...     ['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'], weights=[2, 2, 1],
        ...     rules=RulePlurality(), eliminations=[EliminationLast(k=-2)])
        >>> rule.order_
        [{'a'}, {'b'}, {'c'}, {'d', 'e'}]
    """
    rule = RuleSequentialElimination(
             ['a > b > c > d > e', 'b > a > c > d > e', 'c > a > b > d > e'], weights=[2, 2, 1],
             rules=RulePlurality(), eliminations=[EliminationLast(k=-2)])

    assert rule.order_ == [{'a'}, {'b'}, {'c'}, {'d', 'e'}]

if __name__ == '__main__':
    test_default_elimination()
    test_default_number_of_rounds()
    test_order()
