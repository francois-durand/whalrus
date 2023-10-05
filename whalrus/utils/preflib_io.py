# -*- coding: utf-8 -*-

from whalrus.ballots.ballot_order import BallotOrder


def profile_from_preflib(preflib_file):
    profile = list()
    for line in preflib_file.split("\n"):
        if len(line) == 0:
            continue
        if line[0] == "#":
            continue

        votername = line.split(":")[0].strip()
        order_str = line.split(":")[1].strip()
        order = list()
        while len(order_str) > 0:
            if order_str[0] == "{":
                next_group = order_str[:order_str.find("}")]
                next_group = next_group.replace("{", "")
                next_group = next_group.replace("}", "")
                order.append(
                    {int(candidate) for candidate in next_group.split(",")}
                    )
                order_str = order_str[
                    min(order_str.find("}")+2, len(order_str)):
                    len(order_str)
                    ]
            elif order_str.find(",") != -1:
                next_candidate = order_str[:order_str.find(",")]
                order.append(int(next_candidate))
                order_str = order_str[order_str.find(",")+1 : len(order_str)]
            else:
                order.append(int(order_str))
                break
        profile.append(BallotOrder(order))
    return profile