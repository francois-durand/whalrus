from whalrus.selections.selection_first import SelectionFirst
from whalrus.rules.rule_plurality import RulePlurality
from whalrus.profiles.profile import Profile
from whalrus.converters_ballot.converter_ballot_to_order import ConverterBallotToOrder
from fractions import Fraction
from whalrus.priorities.priority import Priority


def test():

    rule = RulePlurality(ballots=['a > b > c > d', 'b > a > c > d',
        'c > d > b > a', 'd > a > b > c'], weights=[35, 30, 25, 10])

    selection = SelectionFirst(rule=rule, k = 1, threshold = 30)
    assert selection.selected_ == {'a'}

    profile = Profile(ballots = ['b > c > d','b > c > d', 'c > d > b ','d > b > c'],
        weights = [5,30,25,10])
    assert selection.new_profile_.ballots == profile.ballots
    assert selection.new_profile_.weights == profile.weights
   
