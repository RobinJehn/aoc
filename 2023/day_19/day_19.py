from __future__ import annotations
import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache
import copy

np.set_printoptions(threshold=np.inf)


def run(rules, objects, start_rule="in"):
    accepted = []
    for x, m, a, s in objects:
        current_rule = start_rule
        while current_rule != "A" and current_rule != "R":
            specific_rules = rules[current_rule]
            done = False
            for i in range(len(specific_rules) - 1):
                check, result = specific_rules[i]
                if eval(check):
                    done = True
                    current_rule = result
                    break
            if done:
                continue
            current_rule = specific_rules[-1]
        if current_rule == "A":
            accepted.append([x, m, a, s])

    return accepted


def charToIndex(char):
    if char == "x":
        return 0
    elif char == "m":
        return 1
    elif char == "a":
        return 2
    elif char == "s":
        return 3


def split_values(check, values):
    if "<" in check:
        value, limit = check.split("<")
        if values[charToIndex(value)][1] < int(limit):
            return values, []
        elif values[charToIndex(value)][0] >= int(limit):
            return [], values
        else:
            new_values = copy.deepcopy(values)
            new_values[charToIndex(value)][1] = int(limit) - 1
            values[charToIndex(value)][0] = int(limit)
            return new_values, values
    elif ">" in check:
        value, limit = check.split(">")
        if values[charToIndex(value)][0] > int(limit):
            return values, []
        elif values[charToIndex(value)][1] <= int(limit):
            return [], values
        else:
            new_values = copy.deepcopy(values)
            new_values[charToIndex(value)][0] = int(limit) + 1
            values[charToIndex(value)][1] = int(limit)
            return new_values, values
    else:
        return values, []


# List of list of objects
def run_all(rules, current_rule, object):
    if current_rule == "A":
        return [object]
    elif current_rule == "R":
        return []
    objects = []
    specific_rules = rules[current_rule]
    for i in range(len(specific_rules)):
        if i == len(specific_rules) - 1:
            applied = copy.deepcopy(object)
            current_rule = specific_rules[i]
        else:
            check, current_rule = specific_rules[i]
            applied, object = split_values(check, object)
        extra_objects = run_all(rules, current_rule, applied)
        if extra_objects != []:
            objects += extra_objects

    return objects


def part1(data):
    productions = True
    rules = {}
    objects = []
    for line in data:
        if line == "":
            productions = False
            continue
        if productions:
            # Some productions only have one outcome, could optimise
            name, rest = line.split("{")
            rest = rest[:-1]  # remove }
            checks = rest.split(",")
            checks_result = [check.split(":") for check in checks[:-1]]
            checks_result.append(checks[-1])
            rules[name] = checks_result
        else:
            values = line.split(",")
            objects.append(
                [int(value.replace("}", "").split("=")[-1]) for value in values]
            )

    return sum([sum(values) for values in run(rules, objects)])


def part2(data):
    rules = {}
    for line in data:
        if line == "":
            break
        # Some productions only have one outcome, could optimise
        name, rest = line.split("{")
        rest = rest[:-1]  # remove }
        checks = rest.split(",")
        checks_result = [check.split(":") for check in checks[:-1]]
        checks_result.append(checks[-1])
        rules[name] = checks_result

    all = run_all(rules, "in", [[1, 4000], [1, 4000], [1, 4000], [1, 4000]])
    total = 0
    for object in all:
        x_range = object[0][1] - object[0][0] + 1
        m_range = object[1][1] - object[1][0] + 1
        a_range = object[2][1] - object[2][0] + 1
        s_range = object[3][1] - object[3][0] + 1
        total += x_range * m_range * a_range * s_range
    return total

if __name__ == "__main__":
    # file = "2023/day_19/test.txt"
    # file = "test.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
