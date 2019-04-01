from whalrus import RuleRankedPairs, Priority, MatrixRankedPairs


def test():
    rule = RuleRankedPairs(['a > b > c', 'b > c > a', 'c > a > b'], tie_break=Priority.ASCENDING)
    assert rule.strict_order_ == ['a', 'b', 'c']
