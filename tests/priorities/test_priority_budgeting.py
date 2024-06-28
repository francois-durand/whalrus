from whalrus import PriorityBudgeting, PriorityBudgetingAscendingCount
from whalrus import PriorityBudgetingDescendingCost, PriorityBudgetingAscendingCost


def test_count_without_cost():

    priority = PriorityBudgetingAscendingCount()

    assert priority._choose([('p1', 2),('p2', 3)]) == 'p2'
    assert priority._choose([('p1', 2, 100),('p2', 3, 120)]) == 'p2'
    assert priority._choose([('p1', 2, 100),('p2', 2, 120)]) == 'p1'

def test_count_with_lower_cost():
    priority = PriorityBudgetingAscendingCount(cost = True, high = False)
    assert priority._choose([('p1', 2, 100),('p2', 3, 120)]) == 'p2'
    assert priority._choose([('p1', 3, 100),('p2', 3, 120)]) == 'p1'
    assert priority._choose([('p2', 3, 100),('p1', 3, 100)]) == 'p1'

def test_lower_cost_without_count():
    priority = PriorityBudgetingDescendingCost()
    assert priority._choose([('p1', 2, 100),('p2', 1, 120)]) == 'p1' 

def test_lower_cost_with_count():
    priority = PriorityBudgetingDescendingCost(count = True)
    assert priority._choose([('p1', 1, 100),('p2', 2, 120)]) == 'p1' 
    assert priority._choose([('p1', 2, 120),('p2', 3, 120)]) == 'p2' 
 

def test_higher_cost_without_count():
    priority = PriorityBudgetingAscendingCost()
    assert priority._choose([('p1', 2, 100),('p2', 1, 120)]) == 'p2' 

def test_higher_cost_with_count():
    priority = PriorityBudgetingAscendingCost(count = True)
    assert priority._choose([('p1', 2, 100),('p2', 1, 120)]) == 'p2'
    assert priority._choose([('p1', 2, 120),('p2', 1, 120)]) == 'p1' 