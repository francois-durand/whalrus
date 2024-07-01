def equal_shares(voters, projects, cost, u, total_budget):
    
    approvers = {c: [i for i in voters if u[i][c] > 0] for c in projects}
    total_utility = {c: sum(u[i][c] for i in voters) for c in projects}
    mes = equal_shares_fixed_budget(voters, projects, cost, u, total_utility, approvers, total_budget)
    # add1 completion
    # start with integral per-voter budget
    budget = int(total_budget / len(voters)) * len(voters)
    current_cost = sum(cost[c] for c in mes)
    while True:
        # is current outcome exhaustive?
        is_exhaustive = True
        for extra in projects:
            if extra not in mes and current_cost + cost[extra] <= total_budget:
                is_exhaustive = False
                break
        # if so, stop
        if is_exhaustive:
            break
        # would the next highest budget work?
        next_budget = budget + len(voters)
        next_mes = equal_shares_fixed_budget(voters, projects, cost, u, total_utility, approvers, next_budget)
        current_cost = sum(cost[c] for c in next_mes)
        if current_cost <= total_budget:
            # yes, so continue with that budget
            budget = next_budget
            mes = next_mes
        else:
            # no, so stop
            break
    return mes

def break_ties(voters, projects, cost, total_utility, choices):
    remaining = choices.copy()
    best_cost = min(cost[c] for c in remaining)
    remaining = [c for c in remaining if cost[c] == best_cost]
    best_count = max(total_utility[c] for c in remaining)
    remaining = [c for c in remaining if total_utility[c] == best_count]
    return remaining

def equal_shares_fixed_budget(voters, projects, cost, u, total_utility, approvers, total_budget):
    budget = {i: total_budget / len(voters) for i in voters}
    remaining = {} # remaining candidate -> previous effective vote count
    for c in projects:
        if cost[c] > 0 and len(approvers[c]) > 0:
            remaining[c] = total_utility[c]

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
            approvers[c].sort(key=lambda i: budget[i] / u[i][c])
            paid_so_far = 0
            denominator = total_utility[c]
            for i in approvers[c]:
                # compute payment if remaining approvers pay proportional to their utility
                payment_factor = (cost[c] - paid_so_far) / denominator
                eff_vote_count = cost[c] / payment_factor
                if payment_factor * u[i][c] > budget[i]:
                    # i cannot afford the payment, so pays entire remaining budget
                    paid_so_far += budget[i]
                    denominator -= u[i][c]
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
        best = break_ties(voters, projects, cost, total_utility, best)
        if len(best) > 1:
            raise Exception(f"Tie-breaking failed: tie between projects {best} could not be resolved. Another tie-breaking needs to be added.")
        best = best[0]
        winners.append(best)
        del remaining[best]
        # charge the approvers of best
        payment_factor = cost[best] / best_eff_vote_count
        for i in approvers[best]:
            payment = payment_factor * u[i][best]
            if budget[i] > payment:
                budget[i] -= payment
            else:
                budget[i] = 0
    return winners

