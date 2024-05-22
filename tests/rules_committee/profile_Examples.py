from whalrus.profiles.profile import Profile
from whalrus.ballots.ballot_order import BallotOrder
from whalrus.ballots.ballot_levels import BallotLevels


w1 = [4,3,2,1]
k1 = 2

p1 = Profile(['f > e > d > b > c > a', 
       'a > b > c > d > e > f',
       'b > c > a > e > d > f',
         'd > c > a > b > e > f'], weights=w1)

candidates = ['a','b','c','d','e','f','g','h','i','j','k','l']
p2 = Profile(ballots=
[BallotLevels({'a':0,'b':1,'c':0,'d':1,'e':1,'f':0,'g':1,'h':1,'i':0,'j':0,'k':1,'l':0}, candidates = candidates),
 BallotLevels({'a':1,'b':1,'c':0,'d':1,'e':1,'f':1,'g':1,'h':0,'i':1,'j':1,'k':1,'l':1}, candidates = candidates),
 BallotLevels({'a':1,'b':0,'c':1,'d':1,'e':1,'f':0,'g':1,'h':0,'i':0,'j':0,'k':1,'l':1}, candidates = candidates),
BallotLevels({'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':1,'h':0,'i':0,'j':1,'k':1,'l':1}, candidates = candidates),
BallotLevels({'a':1,'b':0,'c':1,'d':1,'e':0,'f':0,'g':1,'h':1,'i':0,'j':0,'k':1,'l':1}, candidates = candidates),
BallotLevels({'a':1,'b':0,'c':0,'d':0,'e':1,'f':1,'g':1,'h':0,'i':0,'j':0,'k':1,'l':1}, candidates = candidates),
BallotLevels({'a':1,'b':1,'c':0,'d':1,'e':1,'f':1,'g':0,'h':1,'i':0,'j':0,'k':1}, candidates = candidates),
BallotLevels({'a':1,'b':1,'c':1,'d':1,'e':1,'f':1,'g':0,'h':0,'i':0,'j':0,'k':1}, candidates = candidates),
BallotLevels({'a':0,'b':1,'c':0,'d':1,'e':1,'f':1,'g':0,'h':0,'i':1,'j':1,'k':1}, candidates = candidates),
BallotLevels({'a':1,'b':1,'c':1,'d':0,'e':0,'f':1,'g':1,'h':1,'i':0,'j':0,'k':1}, candidates = candidates)], weights= [2,1,1,1,1,1,1,1,1,1 ])
candidates2 = ['a','b','c','d']
p_a2 = Profile(ballots=[
    BallotLevels({'a':1, 'b':0,'c':1,'d':0}, candidates = candidates2),
    BallotLevels({'a':1, 'b':0,'c':1,'d':0}, candidates = candidates2),
    BallotLevels({'a':0, 'b':1,'c':0,'d':1}, candidates = candidates2),
    BallotLevels({'a':0, 'b':1,'c':0,'d':0}, candidates = candidates2),
    BallotLevels({'a':0, 'b':1,'c':1,'d':1}, candidates = candidates2),
    BallotLevels({'a':1, 'b':0,'c':0}, candidates = candidates2)])

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
