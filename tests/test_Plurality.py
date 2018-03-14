import pytest
from whalrus import Plurality


def test_plurality_unweighted_winner():
    """Test the Plurality rule (co-winners)"""
    assert Plurality(["A", "A", "B", "A", "C"]).winner() == "A"
    assert Plurality({"e1": "A", "e2": "A", "e3": "B",
                      "e4": "A", "e5": "C"}).winner() == "A"
    # If we use linear orders as input, it should also
    # work as expected
    assert Plurality([["A", "B", "C"],
                      ["A", "B", "C"],
                      ["B", "A", "C"],
                      ["C", "B", "A"],
                      ["A", "B", "C"]]).winner() == "A"
    assert Plurality({"e1": ["A", "B", "C"],
                      "e2": ["A", "B", "C"],
                      "e3": ["B", "A", "C"],
                      "e4": ["C", "B", "A"],
                      "e5": ["A", "B", "C"]}).winner() == "A"


def test_plurality_weighted_winner():
    """Test the Plurality rule (co-winners)"""
    assert Plurality(["A", "A", "B", "A", "C"],
                     weights=[1, 1, 10, 1, 2]).winner() == "B"
    assert Plurality({"e1": "A", "e2": "A", "e3": "B",
                      "e4": "A", "e5": "C"},
                     weights={"e1": 1, "e2": 1, "e3": 10,
                              "e4": 1, "e5": 2}).winner() == "B"
    # If we use an unexpected key in the weight dictionnary,
    # it should raise an exception
    with pytest.raises(KeyError):
        Plurality({"e1": "A", "e2": "A", "e3": "B",
                   "e4": "A", "e5": "C"},
                  weights={"e1": 1, "e2": 1, "e3": 10,
                           "e4": 1, "e6": 2}).winner()
    # If we use linear orders as input, it should also
    # work as expected
    assert Plurality([["A", "B", "C"],
                      ["A", "B", "C"],
                      ["B", "A", "C"],
                      ["C", "B", "A"],
                      ["A", "B", "C"]],
                     weights=[1, 1, 10, 1, 2]).winner() == "B"
    assert Plurality({"e1": ["A", "B", "C"],
                      "e2": ["A", "B", "C"],
                      "e3": ["B", "A", "C"],
                      "e4": ["C", "B", "A"],
                      "e5": ["A", "B", "C"]},
                     weights={"e1": 1, "e2": 1, "e3": 10,
                              "e4": 1, "e5": 2}).winner() == "B"

