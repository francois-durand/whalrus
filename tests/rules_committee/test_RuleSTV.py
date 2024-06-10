from whalrus import RuleSTV, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax
import profile_Examples_c

def test():

    rule = RuleSTV(profile_Examples_c.p1, committee_size = 2)

    assert rule.winning_committee_ == {'a','f'}
    assert rule.eliminated_committee_ == {'b','c','d','e'}
    
    rule = RuleSTV(profile_Examples_c.profile_wiki, committee_size = 3, quota=True)
    assert rule.winning_committee_ == {'Cake','Pears', 'Hamburgers'}