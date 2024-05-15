from whalrus import RuleBucklinByRounds, RuleBucklinInstant, BallotOrder, ScorerBorda, ScorerLevels, ScaleFromList, ConverterBallotToLevels, Profile
from fractions import Fraction

def test_default_median():
    """
         rule = RuleBucklinInstant()
         rule(['a > b'], candidates={'a', 'b', 'c'}).scores_
        {'a': (2, 1), 'b': (1, 1), 'c': (0, 0)}
    """

    rule = RuleBucklinInstant()
    assert rule(['a > b'], candidates={'a', 'b', 'c'}).scores_ == {'a': (2, 1), 'b': (1, 1), 'c': (0, 0)}


def test_same_score():
    """
         rule = RuleBucklinInstant()
         rule.compare_scores((2, 1), (2, 1))
        0
    """
    
    rule = RuleBucklinInstant()
    assert rule.compare_scores((2, 1), (2, 1)) == 0


def test_scores_as_floats():
    """
         rule = RuleBucklinInstant(
        ...     converter=ConverterBallotToLevels(),
        ...     scorer=ScorerLevels(
        ...         scale=ScaleFromList(['To Reject', 'Poor', 'Acceptable', 'Good', 'Very Good', 'Excellent'])
        ...     )
        ... )
         rule([{'a': 'Very Good', 'b': 'Acceptable'}]).scores_as_floats_
        {'a': ('Very Good', 1.0), 'b': ('Acceptable', 1.0)}
    """
    

    rule = RuleBucklinInstant(
           converter=ConverterBallotToLevels(),
             scorer=ScorerLevels(
                 scale=ScaleFromList(['To Reject', 'Poor', 'Acceptable', 'Good', 'Very Good', 'Excellent'])
             )
         )

    assert rule([{'a': 'Very Good', 'b': 'Acceptable'}]).scores_as_floats_ == {'a': ('Very Good', 1.0), 'b': ('Acceptable', 1.0)}

def test():

    rule = RuleBucklinInstant(ballots=['a > b > c', 'b > a > c', 'c > a > b'])
    assert rule.scores_ ==  {'a': (1, 3), 'b': (1, 2), 'c': (0, 3)}
    assert rule.winner_ == 'a'

    profile = Profile(ballots=['a > b > c > d', 'b > a ~ d > c', 'c > a ~ d > b'],
                           weights=[3, 3, 4])
    rule_bucklin_by_rounds = RuleBucklinByRounds(profile)
    assert rule_bucklin_by_rounds.detailed_scores_[0] == {'a': Fraction(3, 10), 'b': Fraction(3, 10), 'c': Fraction(2, 5), 'd': 0}
    assert rule_bucklin_by_rounds.detailed_scores_[1] == {'a': Fraction(13, 20), 'b': Fraction(3, 5), 'c': Fraction(2, 5), 'd': Fraction(7, 20)}
    assert rule_bucklin_by_rounds.winner_ == 'a'
    rule_bucklin_instant = RuleBucklinInstant(profile)
    assert rule_bucklin_instant.scores_ == {'a': (Fraction(3, 2), 10), 'b': (2, 6), 'c': (1, 7), 'd': (Fraction(3, 2), 7)}
    assert RuleBucklinInstant(profile).winner_ == 'b'

if __name__ == '__main__':
    test()
    test_default_median()
    test_same_score()   
    test_scores_as_floats()