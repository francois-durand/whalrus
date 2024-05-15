from whalrus import RuleScorePositional
from whalrus.rules.rule_score_num_average import RuleScoreNumAverage
from whalrus.scorers.scorer_positional import ScorerPositional
from whalrus.converters_ballot.converter_ballot_to_strict_order import ConverterBallotToStrictOrder
from whalrus.priorities.priority import Priority
from whalrus.converters_ballot.converter_ballot import ConverterBallot


def test():

    rule = RuleScorePositional(['a > b > c', 'b > c > a'], points_scheme=[3, 2, 1])
    assert rule.gross_scores_ ==  {'a': 4, 'b': 5, 'c': 3}


    rule = RuleScorePositional(['a > b ~ c', 'b > c > a'], points_scheme=[1, 1, 0],
      converter=ConverterBallotToStrictOrder(priority=Priority.ASCENDING))
    assert rule.gross_scores_ == {'a': 1, 'b': 2, 'c': 1}

if __name__ == '__main__':
    test()

    