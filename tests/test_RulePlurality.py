from whalrus.rule.RulePlurality import RulePlurality
from whalrus.ballot.BallotOneName import BallotOneName
from whalrus.priority.Priority import Priority


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
    assert plurality(profile).gross_scores_ == {'A': 4, 'B': 2, 'C': 1, 'D': 0}
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


def test_as_a_committee_rule():
    plurality = RulePlurality(
        ballots=['a', 'b', 'c', 'd', 'e'],
        weights=[2, 3, 1, 3, 1],
        tie_break=Priority.ASCENDING
    )
    # As a single-winner rule
    assert plurality.order_ == [{'b', 'd'}, {'a'}, {'c', 'e'}]
    assert plurality.strict_order_ == ['b', 'd', 'a', 'c', 'e']
    assert plurality.cotrailers_ == {'c', 'e'}
    assert plurality.trailer_ == 'e'
    assert plurality.cowinners_ == {'b', 'd'}
    assert plurality.winner_ == 'b'
    # As a committee rule

    def singleton(c):
        return frozenset({c})
    assert plurality.order_on_committees_ == [{singleton('b'), singleton('d')},
                                              {singleton('a')},
                                              {singleton('c'), singleton('e')}]
    assert plurality.strict_order_on_committees_ == [
        singleton('b'), singleton('d'), singleton('a'), singleton('c'), singleton('e')]
    assert plurality.cotrailing_committees_ == {singleton('c'), singleton('e')}
    assert plurality.trailing_committee_ == singleton('e')
    assert plurality.cowinning_committees_ == {singleton('b'), singleton('d')}
    assert plurality.winning_committee_ == singleton('b')


def test_exact_precision():
    plurality = RulePlurality(ballots=['a', 'b', 'c', 'd'], weights=[35, 30, 25, 10])
    assert sum(plurality.scores_.values()) == 1


def test_random_tie_break():
    for i in range(5):
        rule = RulePlurality(['a', 'b'], tie_break=Priority.RANDOM)
        assert rule.winner_ == rule.strict_order_[0]


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
