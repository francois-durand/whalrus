from whalrus import RuleBucklinInstant, BallotOrder, ScorerBorda, ScorerLevels, ScaleFromList, ConverterBallotToLevels


def test_default_median():
    """
        >>> rule = RuleBucklinInstant()
        >>> rule(['a > b'], candidates={'a', 'b', 'c'}).scores_
        {'a': (2, 1), 'b': (1, 1), 'c': (0, 0)}
    """
    pass


def test_same_score():
    """
        >>> rule = RuleBucklinInstant()
        >>> rule.compare_scores((2, 1), (2, 1))
        0
    """
    pass


def test_scores_as_floats():
    """
        >>> rule = RuleBucklinInstant(
        ...     converter=ConverterBallotToLevels(),
        ...     scorer=ScorerLevels(
        ...         scale=ScaleFromList(['To Reject', 'Poor', 'Acceptable', 'Good', 'Very Good', 'Excellent'])
        ...     )
        ... )
        >>> rule([{'a': 'Very Good', 'b': 'Acceptable'}]).scores_as_floats_
        {'a': ('Very Good', 1.0), 'b': ('Acceptable', 1.0)}
    """
    pass
