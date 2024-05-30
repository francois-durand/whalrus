from whalrus.profiles.profile import Profile
from whalrus.ballots.ballot_levels import BallotLevels
from whalrus.ballots.ballot_order import BallotOrder

#w_a1 = [24,21,24,23,22,25]
w_a1 = [2,1,1,1,1,1]
p_a1 = Profile([{'a':1, 'b':0,'c':1,'d':0},{'a':1, 'b':0,'c':1,'d':0},

        {'a':0, 'b':1,'c':0,'d':1}, {'a':0, 'b':1,'c':0,'d':0},
        {'a':0, 'b':1,'c':1,'d':1}, {'a':1, 'b':0,'c':0}], weights = w_a1)

candidates = ['a','b','c','d']

p_a2 = Profile(ballots=[
    BallotLevels({'a':1, 'b':0,'c':1}),
    BallotLevels({'a':1, 'b':0,'c':1}),
    BallotLevels({'a':0, 'b':1,'c':0,'d':1}),
    BallotLevels({'a':0, 'b':1,'c':0}),
    BallotLevels({'a':0, 'b':1,'c':1,'d':1}),
    BallotLevels({'a':1, 'b':0,'c':0})])

candidates = {'Oranges','Pears', 'Strawberries', 'Cake', 'Chocolate', 'Hamburgers', 'Chicken'}
b1 = BallotOrder(['Oranges', 'Pears'], candidates = candidates)
b2 = BallotOrder(['Pears','Strawberries', 'Cake'], candidates = candidates)
b3 = BallotOrder(['Strawberries', 'Oranges',' Pears'], candidates = candidates)
b4 = BallotOrder(['Cake','Chocolate'], candidates = candidates)
b5 = BallotOrder(['Chocolate','Cake', 'Hamburgers'], candidates = candidates)
b6 = BallotOrder(['Hamburgers','Chicken'], candidates = candidates)
b7 = BallotOrder(['Chicken','Chocolate', 'Hamburgers'], candidates = candidates)

w = [3,8,1,3,1,4,3]


profile_wiki = Profile(ballots=[b1,b2,b3,b4,b5,b6,b7], weights = w)
