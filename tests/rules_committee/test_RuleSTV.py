from whalrus import RuleSTV, RulePlurality
from whalrus import Priority, PriorityLiftedLeximax
import profile_Examples

def test():

    rule = RuleSTV(profile_Examples.profile_stv, committee_size = 2)

    print(rule.stv_())

if __name__ == '__main__':
    test()