from whalrus.rule.RuleMaximin import RuleMaximin


def test():
    # FIXED BUG
    # The reason of this bug was that all instances of ``RuleMaximin`` used to share the same
    # ``MatrixWeightedMajority()`` (which was the default argument for ``matrix_weighted_majority``).
    rule1 = RuleMaximin(ballots=['a > b'])
    rule2 = RuleMaximin(ballots=['b > a'])
    assert rule1.matrix_weighted_majority_.as_dict_[('a', 'b')] == 1
    assert rule2.matrix_weighted_majority_.as_dict_[('a', 'b')] == 0
    assert rule1.matrix_weighted_majority_.as_dict_[('a', 'b')] == 1
