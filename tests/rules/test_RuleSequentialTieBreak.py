from whalrus import RuleBorda, RulePlurality, Priority, RuleSequentialTieBreak

def test():
    # Cf. docstring.
    rule = RuleSequentialTieBreak(
             ['a > d > e > b > c', 'b > d > e > a > c', 'c > d > e > a > b',
              'd > e > b > a > c', 'e > d > b > a > c'],
             weights=[2, 2, 2, 1, 1],
             rules=[RulePlurality(), RuleBorda()], tie_break=Priority.ASCENDING)
    assert  rule.rules_[0].gross_scores_ == {'a': 2, 'b': 2, 'c': 2, 'd': 1, 'e': 1}
    assert  rule.rules_[1].gross_scores_ == {'a': 14, 'b': 14, 'c': 8, 'd': 25, 'e': 19}
    assert  rule.order_ == [{'a', 'b'}, {'c'}, {'d'}, {'e'}]
    assert  rule.winner_ == 'a'

if __name__ == '__main__':
    test()
