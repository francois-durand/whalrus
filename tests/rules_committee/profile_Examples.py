from whalrus.profiles.profile import Profile
from whalrus.ballots.ballot_order import BallotOrder

p1 = Profile(['f > e > d > b > c > a', 'f > e > d > b > c > a',
      'f > e > d > b > c > a' ,'f > e > d > b > c > a',
       'a > b > c > d > e > f','a > b > c > d > e > f',
       'a > b > c > d > e > f',
       'b > c > a > e > d > f', 'b > c > a > e > d > f'
       , 'd > c > a > b > e > f'])

w1 = [4,3,2,1]
k1 = 2


candidates = ['Oranges','Pears', 'Strawberries', 'Cake', 'Chocolate', 'Hamburgers', 'Chicken']
p2 = Profile(['Oranges > Pears','Oranges > Pears','Oranges > Pears',
      'Pears > Strawberries > Cake','Pears > Strawberries > Cake','Pears > Strawberries > Cake',
      'Pears > Strawberries > Cake','Pears > Strawberries > Cake','Pears > Strawberries > Cake',
      'Pears > Strawberries > Cake','Pears > Strawberries > Cake',
      'Strawberries > Oranges > Pears',
      'Cake > Chocolate', 'Cake > Chocolate', 'Cake > Chocolate', 
      'Chocolate > Cake > Hamburgers',
      'Hamburgers > Chicken','Hamburgers > Chicken','Hamburgers > Chicken',
      'Hamburgers > Chicken',
      'Chicken > Chocolate > Hamburgers','Chicken > Chocolate > Hamburgers','Chicken > Chocolate > Hamburgers'],
      candidates = candidates)