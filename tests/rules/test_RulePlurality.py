from math import isclose
from fractions import Fraction
from whalrus import RulePlurality, BallotOneName, Priority, ScorerVeto, BallotVeto, ScorerPlurality


def test():
    plurality = RulePlurality()

    profile = [
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["B", "A", "C"],
        ["C", "B", "A"],
        ["A", "B", "C"],
        {'A': 10, 'B': 7, 'C': 0},
        'B > A ~ C > D'
    ]
    plurality(profile)
    assert plurality.gross_scores_ == {'A': 4, 'B': 2, 'C': 1, 'D': 0}
    assert plurality.scores_ == {'A': Fraction(4, 7), 'B': Fraction(2, 7), 'C': Fraction(1, 7), 'D': 0}
    assert plurality.best_score_ == Fraction(4, 7)
    assert plurality.worst_score_ == 0
    assert plurality.average_score_ == Fraction(1, 4)
    assert plurality.gross_scores_as_floats_ == {'A': 4., 'B': 2., 'C': 1., 'D': 0.}
    assert plurality.weights_as_floats_ == {'A': 7., 'B': 7., 'C': 7., 'D': 7.}
    assert isclose(plurality.best_score_as_float_, 4/7)
    assert plurality.worst_score_as_float_ == 0.
    assert isclose(plurality.average_score_as_float_, 1/4)
    assert plurality.order_ == [{'A'}, {'B'}, {'C'}, {'D'}]
    assert plurality(profile, candidates={'A', 'B', 'D'}).gross_scores_ == {'A': 4, 'B': 3, 'D': 0}

    profile = [None, None, 'b', 42]
    assert plurality(profile).gross_scores_ == {'b': 1, 42: 1}

    profile = ['a', 'a > b ~ c', 'b', ['c', 'b'], 42]
    assert plurality(profile).gross_scores_ == {'a': 2, 'b': 1, 'c': 1, 42: 1}

    profile = [
        'a > b > c',
        'c > b > a',
    ]
    assert plurality(profile, candidates={'b', 'c'}).gross_scores_ == {'b': 1, 'c': 1}
    assert plurality(profile, candidates={'a', 'b', 'c', 'd'}).gross_scores_ == {'a': 1, 'b': 0, 'c': 1, 'd': 0}
    assert plurality(profile, candidates={'b', 'c', 'd'}).gross_scores_ == {'b': 1, 'c': 1, 'd': 0}


def test_order_and_trailers():
    plurality = RulePlurality(
        ballots=['a', 'b', 'c', 'd', 'e'],
        weights=[2, 3, 1, 3, 1],
        tie_break=Priority.ASCENDING
    )
    assert plurality.order_ == [{'b', 'd'}, {'a'}, {'c', 'e'}]
    assert plurality.strict_order_ == ['b', 'd', 'a', 'c', 'e']
    assert plurality.cotrailers_ == {'c', 'e'}
    assert plurality.trailer_ == 'e'


def test_trailer_one_candidate():
    """
        >>> plurality = RulePlurality(['a'])
        >>> plurality.trailer_
        'a'
    """
    pass


def test_exact_precision():
    plurality = RulePlurality(ballots=['a', 'b', 'c', 'd'], weights=[35, 30, 25, 10])
    assert sum(plurality.scores_.values()) == 1


def test_random_tie_break():
    """
        >>> class PriorityPseudoRandom(Priority):
        ...     def __init__(self):
        ...         super().__init__(name='Pseudo-random')
        ...     def _sort(self, x, reverse):
        ...         return ['a', 'b', 'c', 'd']
        ...     def _choice(self, x, reverse):
        ...         if reverse:
        ...             return 'c'
        ...         else:
        ...             return 'b'
        >>> rule = RulePlurality(['a', 'b', 'c', 'd'], tie_break=PriorityPseudoRandom())
        >>> rule.winner_
        'b'
        >>> rule.trailer_
        'c'

    The strict_order_ given by the random tie-break is corrected in order to be consistent with winner_ and trailer_:

        >>> rule.strict_order_
        ['b', 'a', 'd', 'c']
    """
    pass


def test_scorer_not_plurality():
    """
    A strange voting rule where the candidate with most vetos wins!

        >>> rule = RulePlurality(scorer=ScorerVeto())
        >>> rule([BallotVeto('a', candidates={'a', 'b'})]).winner_
        'a'
    """
    pass


def test_count_abstention():
    """
        >>> rule = RulePlurality(scorer=ScorerPlurality(count_abstention=True))
        >>> rule(['a', 'a', 'b', None]).scores_
        {'a': Fraction(1, 2), 'b': Fraction(1, 4)}
    """
    pass


def test_compare():
    """
        >>> rule = RulePlurality()
        >>> rule.compare_scores(42, 42)
        0
        >>> rule.compare_scores(51, 42)
        1
    """
    pass


def test_old_plurality_unweighted_winner():
    assert RulePlurality(["A", "A", "B", "A", "C"]).winner_ == "A"
    assert RulePlurality(["A", "A", "B", "C", "", "", ""]).winner_ == "A"
    assert RulePlurality(["A", "A", "B", "A", "C"], voters=['e1', 'e2', 'e3', 'e4', 'e5']).winner_ == 'A'
    # If we use linear orders as input, it should also work as expected
    assert RulePlurality([
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["B", "A", "C"],
        ["C", "B", "A"],
        ["A", "B", "C"]
    ]).winner_ == "A"
    assert RulePlurality([
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["B", "A", "C"],
        ["C", "B", "A"],
        ["A", "B", "C"]
    ], voters=['e1', 'e2', 'e3', 'e4', 'e5']).winner_ == "A"


def test_old_plurality_weighted_winner():
    assert RulePlurality(["A", "A", "B", "A", "C"], weights=[1, 1, 10, 1, 2]).winner_ == "B"
    assert RulePlurality(
        ["A", "A", "B", "A", "C", "", "", ""],
        weights=[1, 1, 10, 1, 2, 1, 42, 1]
    ).winner_ == "B"
    assert RulePlurality(
        ["A", "A", "B", "A", "C"],
        weights=[1, 1, 10, 1, 2],
        voters=['e1', 'e2', 'e3', 'e4', 'e5']
    ).winner_ == "B"
    # If we use linear orders as input, it should also work as expected
    assert RulePlurality([
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["B", "A", "C"],
        ["C", "B", "A"],
        ["A", "B", "C"]
    ], weights=[1, 1, 10, 1, 2]).winner_ == "B"
    assert RulePlurality([
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["B", "A", "C"],
        ["C", "B", "A"],
        ["A", "B", "C"]
    ], weights=[1, 1, 10, 1, 2], voters=['e1', 'e2', 'e3', 'e4', 'e5']).winner_ == "B"
    assert RulePlurality([
        BallotOneName("A"),
        BallotOneName("A"),
        BallotOneName("B"),
        BallotOneName("A"),
        BallotOneName("C")
    ], weights=[1, 1, 10, 1, 2]).winner_ == "B"


def test_old_plurality_unweighted_cowinners():
    """Test the unweighted Plurality rule (co-winners)"""
    assert "A" in RulePlurality(["A", "A", "B", "A", "C", "B", "B"]).cowinners_
    assert "B" in RulePlurality(["A", "A", "B", "A", "C", "B", "B"]).cowinners_
    assert "A" in RulePlurality(["A", "A", "B", "C", "C", "", ""]).cowinners_
    assert "C" in RulePlurality(["A", "A", "B", "C", "C", "", ""]).cowinners_
    assert "A" in RulePlurality(["A", "A", "B", "A", "C"], voters=['e1', 'e2', 'e3', 'e4', 'e5']).cowinners_
    # If we use linear orders as input, it should also work as expected
    assert "A" in RulePlurality([
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["B", "A", "C"],
        ["B", "C", "A"],
        ["A", "B", "C"]
    ]).cowinners_
    assert "A" in RulePlurality([
        ["A", "B", "C"],
        ["A", "B", "C"],
        ["B", "A", "C"],
        ["B", "C", "A"],
        ["A", "B", "C"]
    ], voters=['e1', 'e2', 'e3', 'e4', 'e5']).cowinners_
