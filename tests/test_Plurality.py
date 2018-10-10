def test_plurality_unweighted_winner():
    # """Test the unweighted Plurality rule (single winner)"""
    # assert Plurality(["A", "A", "B", "A", "C"]).winner() == "A"
    # assert Plurality(["A", "A", "B", "C", "", "", ""]).winner() == "A"
    # assert Plurality({"e1": "A", "e2": "A", "e3": "B",
    #                   "e4": "A", "e5": "C"}).winner() == "A"
    # # If we use linear orders as input, it should also
    # # work as expected
    # assert Plurality([["A", "B", "C"],
    #                   ["A", "B", "C"],
    #                   ["B", "A", "C"],
    #                   ["C", "B", "A"],
    #                   ["A", "B", "C"]]).winner() == "A"
    # assert Plurality({"e1": ["A", "B", "C"],
    #                   "e2": ["A", "B", "C"],
    #                   "e3": ["B", "A", "C"],
    #                   "e4": ["C", "B", "A"],
    #                   "e5": ["A", "B", "C"]}).winner() == "A"
    pass


def test_plurality_weighted_winner():
    # """Test the weighted Plurality rule (single winner)"""
    # assert Plurality(["A", "A", "B", "A", "C"],
    #                  weights=[1, 1, 10, 1, 2]).winner() == "B"
    # assert Plurality(["A", "A", "B", "A", "C", "", "", ""],
    #                  weights=[1, 1, 10, 1, 2, 1, 42, 1]).winner() == "B"
    # assert Plurality({"e1": "A", "e2": "A", "e3": "B",
    #                   "e4": "A", "e5": "C"},
    #                  weights={"e1": 1, "e2": 1, "e3": 10,
    #                           "e4": 1, "e5": 2}).winner() == "B"
    # # If we use an unexpected key in the weight dictionnary,
    # # it should raise an exception
    # with pytest.raises(KeyError):
    #     Plurality({"e1": "A", "e2": "A", "e3": "B",
    #                "e4": "A", "e5": "C"},
    #               weights={"e1": 1, "e2": 1, "e3": 10,
    #                        "e4": 1, "e6": 2}).winner()
    # # If we use linear orders as input, it should also
    # # work as expected
    # assert Plurality([["A", "B", "C"],
    #                   ["A", "B", "C"],
    #                   ["B", "A", "C"],
    #                   ["C", "B", "A"],
    #                   ["A", "B", "C"]],
    #                  weights=[1, 1, 10, 1, 2]).winner() == "B"
    # assert Plurality({"e1": ["A", "B", "C"],
    #                   "e2": ["A", "B", "C"],
    #                   "e3": ["B", "A", "C"],
    #                   "e4": ["C", "B", "A"],
    #                   "e5": ["A", "B", "C"]},
    #                  weights={"e1": 1, "e2": 1, "e3": 10,
    #                           "e4": 1, "e5": 2}).winner() == "B"
    #
    # assert Plurality([SingleCandidateBallot("A", 1),
    #                   SingleCandidateBallot("A", 1),
    #                   SingleCandidateBallot("B", 10),
    #                   SingleCandidateBallot("A", 1),
    #                   SingleCandidateBallot("C", 2)]).winner() == "B"
    pass


def test_plurality_unweighted_cowinners():
    # """Test the unweighted Plurality rule (co-winners)"""
    # assert "A" in Plurality(["A", "A", "B", "A", "C", "B", "B"]).cowinners()
    # assert "B" in Plurality(["A", "A", "B", "A", "C", "B", "B"]).cowinners()
    # assert "A" in Plurality(["A", "A", "B", "C", "C", "", ""]).cowinners()
    # assert "C" in Plurality(["A", "A", "B", "C", "C", "", ""]).cowinners()
    # assert "A" in Plurality({"e1": "A", "e2": "A", "e3": "B",
    #                          "e4": "A", "e5": "C"}).cowinners()
    # # If we use linear orders as input, it should also
    # # work as expected
    # assert "A" in Plurality([["A", "B", "C"],
    #                          ["A", "B", "C"],
    #                          ["B", "A", "C"],
    #                          ["B", "C", "A"],
    #                          ["A", "B", "C"]]).cowinners()
    # assert "B" in  Plurality({"e1": ["A", "B", "C"],
    #                           "e2": ["A", "B", "C"],
    #                           "e3": ["B", "A", "C"],
    #                           "e4": ["B", "C", "A"],
    #                           "e5": ["A", "B", "C"]}).cowinners()
    pass
