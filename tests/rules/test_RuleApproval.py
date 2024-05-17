from whalrus import RuleApproval
import profile_Examples


def test():
    # Test with a ballot conversion:
    assert RuleApproval(['a > b > c > d', 'c > a > b > d']).gross_scores_ == {'a': 2, 'b': 1, 'c': 1, 'd': 0}

    print(RuleApproval(profile_Examples.p_a2).scores_)
    

if __name__ == '__main__':

    test()
