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
    
def test_count_sort():
    priority = PriorityBudgetingAscendingCount(cost = False)
    assert priority._sort([('p1', 2, 100),('p2', 3, 120)]) == ["p2","p1"]
    assert priority._sort([('p1', 3, 100),('p2', 3, 120)]) == ["p1","p2"]

    priority = PriorityBudgetingAscendingCount(cost = True, high = True)
    assert priority._sort([('p1', 2, 120),('p2', 5, 120),('p3',4,150)]) == ['p2','p3','p1']
    assert priority._sort([('p1', 2, 120),('p2', 2, 120),('p3',4,120)]) == ['p3','p1','p2']
  
    priority = PriorityBudgetingAscendingCount(cost = True, high = False)
    assert priority._sort([('p1', 2, 120),('p2', 5, 120),('p3',4,150)]) == ['p2','p3','p1']
    assert priority._sort([('p1', 2, 160),('p2', 2, 120),('p3',4,140)]) == ['p3','p2','p1']

def test_lower_cost_without_count():
    priority = PriorityBudgetingDescendingCost()
    assert priority._choose([('p1', 2, 100),('p2', 1, 120)]) == 'p1' 

def test_lower_cost_with_count():
    priority = PriorityBudgetingDescendingCost(count = True)
    assert priority._choose([('p1', 1, 100),('p2', 2, 120)]) == 'p1' 
    assert priority._choose([('p1', 2, 120),('p2', 3, 120)]) == 'p2' 
 
def test_lower_cost_sort():
    priority = PriorityBudgetingDescendingCost(count = False)
    assert priority._sort([('p1', 1, 120),('p2', 2, 100)]) == ['p2', 'p1']
    assert priority._sort([('p1', 2, 100),('p2', 3, 100)]) == ['p1','p2'] 

    priority = PriorityBudgetingDescendingCost(count = True)
    assert priority._sort([('p1', 2, 120),('p2', 1, 120),('p3',4,150)]) == ['p1','p2','p3']
    assert priority._sort([('p1', 2, 120),('p2', 2, 120),('p3',4,120)]) == ['p3','p1','p2']

def test_higher_cost_without_count():
    priority = PriorityBudgetingAscendingCost()
    assert priority._choose([('p1', 2, 100),('p2', 1, 120)]) == 'p2' 

def test_higher_cost_with_count():
    priority = PriorityBudgetingAscendingCost(count = True)
    assert priority._choose([('p1', 2, 100),('p2', 1, 120)]) == 'p2'
    assert priority._choose([('p1', 2, 120),('p2', 1, 120)]) == 'p1' 

def test_higher_cost_sort():
    priority = PriorityBudgetingAscendingCost(count = False)
    assert priority._sort([('p1', 2, 100),('p2', 1, 120)]) == ['p2','p1']
    assert priority._sort([('p1', 2, 120),('p2', 1, 120)]) == ['p1','p2']

    priority = PriorityBudgetingAscendingCost(count = True)
    assert priority._sort([('p1', 2, 120),('p2', 1, 120),('p3',4,150)]) == ['p3','p1','p2']
    assert priority._sort([('p1', 2, 120),('p2', 2, 120),('p3',4,120)]) == ['p3','p1','p2']
