from whalrus.participatories_budgeting.mes_add1 import MesAdd1

from whalrus.participatories_budgeting.greedy import Greedy
from whalrus.profiles.profile import Profile
from whalrus.converters_ballot.converter_ballot_to_levels_interval import ConverterBallotToLevelsInterval 
from whalrus.scales.scale_interval import ScaleInterval

def equal_shares(voters, projects, cost, approvers, total_budget):

    mes = equal_shares_fixed_budget(voters, projects, cost, approvers, total_budget)
    # add1 completion
    budget = total_budget
    while True:
        # would the next highest budget work?
        next_budget = budget + len(voters)
        next_mes = equal_shares_fixed_budget(voters, projects, cost, approvers, next_budget)
        if sum(cost[c] for c in next_mes) <= total_budget:
            # yes, so continue with that budget
            budget = next_budget
            mes = next_mes
        else:
            # no, so stop
            break
    return mes

def break_ties(voters, projects, cost, approvers, choices):
    remaining = choices.copy()
    best_cost = min(cost[c] for c in remaining)
    remaining = [c for c in remaining if cost[c] == best_cost]
    best_count = max(len(approvers[c]) for c in remaining)
    remaining = [c for c in remaining if len(approvers[c]) == best_count]
    return remaining

def equal_shares_fixed_budget(voters, projects, cost, approvers, total_budget):
    budget = {i: total_budget / len(voters) for i in voters}
    remaining = {} # remaining candidate -> previous effective vote count
    for c in projects:
        if cost[c] > 0 and len(approvers[c]) > 0:
            remaining[c] = len(approvers[c])
    winners = []
    while True:
        best = []
        best_eff_vote_count = 0
        # go through remaining candidates in order of decreasing previous effective vote count
        remaining_sorted = sorted(remaining, key=lambda c: remaining[c], reverse=True)
        for c in remaining_sorted:
            previous_eff_vote_count = remaining[c]
            if previous_eff_vote_count < best_eff_vote_count:
                # c cannot be better than the best so far
                break
            money_behind_now = sum(budget[i] for i in approvers[c])
            if money_behind_now < cost[c]:
                # c is not affordable
                del remaining[c]
                continue
            # calculate the effective vote count of c
            approvers[c].sort(key=lambda i: budget[i])
            paid_so_far = 0
            denominator = len(approvers[c])
            for i in approvers[c]:
                # compute payment if remaining approvers pay equally
                max_payment = (cost[c] - paid_so_far) / denominator
                eff_vote_count = cost[c] / max_payment
                if max_payment > budget[i]:
                    # i cannot afford the payment, so pays entire remaining budget
                    paid_so_far += budget[i]
                    denominator -= 1
                else:
                    # i (and all later approvers) can afford the payment; stop here
                    remaining[c] = eff_vote_count
                    if eff_vote_count > best_eff_vote_count:
                        best_eff_vote_count = eff_vote_count
                        best = [c]
                    elif eff_vote_count == best_eff_vote_count:
                        best.append(c)
                    break
        if not best:
            # no remaining candidates are affordable
            break
        best = break_ties(voters, projects, cost, approvers, best)
        if len(best) > 1:
            raise Exception(f"Tie-breaking failed: tie between projects {best} could not be resolved. Another tie-breaking needs to be added.")
        best = best[0]
        winners.append(best)
        del remaining[best]
        # charge the approvers of best
        best_max_payment = cost[best] / best_eff_vote_count
        for i in approvers[best]:
            if budget[i] > best_max_payment:
                budget[i] -= best_max_payment
            else:
                budget[i] = 0
    return winners
# if __name__ == "__main__":
#     p = Profile([{'a':2,'b':2,'c':0,'d':0,'e':-2},
#             {'a':0,'b':0,'c':0,'d':0,'e':2}
#         ])
    
#     cc = MesAdd1(p, project_cost = {'a':5,'b':12,'c':15,'d':20,'e':25}, budget = 50, converter = ConverterBallotToLevelsInterval(scale = ScaleInterval(low = 0, high = 2)))
    
