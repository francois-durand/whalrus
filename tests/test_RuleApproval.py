from whalrus import RuleApproval


def test():
    # Test with a ballot conversion:
    assert RuleApproval(['a > b > c > d', 'c > a > b > d']).gross_scores_ == {'a': 2, 'b': 1, 'c': 1, 'd': 0}
