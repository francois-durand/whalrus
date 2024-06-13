from whalrus.selections.selection_above import SelectionAbove
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.profiles.profile import Profile
from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
from fractions import Fraction
from whalrus.priorities.priority import Priority

def test():

    rule = RulePlurality(ballots=['a > b > c > d', 'b > a > c > d',
        'c > d > b > a', 'd > a > d > c'], weights=[35, 30, 25, 10])

    selection = SelectionAbove(rule=rule, threshold = 30)
    assert selection.selected_ == {'a','b'}

    assert selection.new_profile_ == Profile(ballots = ['c > d','d > c', 'c > d'],
        weights = [Fraction(35/6),25,10])


if __name__ == '__main__':

    w1 = [4,3,2,1]

    p1 = Profile(['f > e > d > b > c > a', 
        'a > b > c > d > e > f',
        'b > c > a > e > d > f',
            'd > c > a > b > e > f'], weights=w1)
    rule = RulePlurality(tie_break = Priority.ASCENDING,converter = ConverterBallotToOrder())
    rule(p1)
    selection = SelectionAbove(rule=rule, threshold = 30)
    print(rule.profile_converted_)
    print(selection.new_profile_)