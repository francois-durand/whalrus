# -*- coding: utf-8 -*-

from whalrus.ballots.ballot_order import BallotOrder


def profile_from_preflib(raw_data=None, file_path=None):
    if raw_data == None and file_path == None:
        raise ValueError("Either raw_data or file_path must be specified.")
    if raw_data == None:
        f = open(file_path, "r")
        raw_data = f.read()
        f.close()
    
    # Check Datatype
    if raw_data.find("# DATA TYPE") != -1:
        raw_data = raw_data[raw_data.find("# Data Type") + 11:]
        dtype = raw_data[:raw_data.find("\n")]
        if not ("toc" in dtype or "toi" in dtype or "soi" in dtype or "soc" in dtype):
            raise ValueError("The input describes an unsupported datatype.", dtype)
    else:
         raise ValueError("The input has unknown datatype.")

    # Load Metadata
    alternatives = dict()
    while raw_data.find("# ALTERNATIVE NAME") != -1:
        raw_data = raw_data[raw_data.find("# ALTERNATIVE NAME") + 18:]
        alternative_num = int(raw_data[:raw_data.find(":")])
        raw_data = raw_data[raw_data.find(":") + 1:]
        alternative_name = raw_data[:raw_data.find("\n")]
        raw_data = raw_data[raw_data.find("\n"):]
        alternatives[alternative_num] = alternative_name

    # Load Profile
    profile = list()
    for line in raw_data.split("\n"):
        if len(line) == 0:
            continue
        if line[0] == "#":
            continue

        multiplicity = int(line.split(":")[0].strip())
        order_str = line.split(":")[1].strip()
        order = list()
        while len(order_str) > 0:
            if order_str[0] == "{":
                next_group = order_str[:order_str.find("}")]
                next_group = next_group.replace("{", "")
                next_group = next_group.replace("}", "")
                if len(next_group) > 0:
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
        for i in range(multiplicity):
            profile.append(BallotOrder(order, candidates=alternatives.keys()))
    return profile