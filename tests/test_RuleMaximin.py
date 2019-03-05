from whalrus.rule.RuleMaximin import RuleMaximin


def test():
    # The test below illustrates a bug. The reason is tha all instances of ``RuleMaximin`` share the same
    # ``MatrixWeightedMajority()`` (default argument for ``matrix_weighted_majority``).
    rule1 = RuleMaximin(ballots=['a > b'])
    rule2 = RuleMaximin(ballots=['b > a'])
    assert rule1.matrix_weighted_majority_.as_dict_[('a', 'b')] == 1.0
    assert rule2.matrix_weighted_majority_.as_dict_[('a', 'b')] == 0.0
    assert rule1.matrix_weighted_majority_.as_dict_[('a', 'b')] == 1.0
