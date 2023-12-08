import math
import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict


def part1(data):
    moves = list(map(lambda x: 0 if x == "L" else 1, data[0]))
    maps = defaultdict(list)
    for line in data[2:]:
        key, value = line.replace(" ", "").split("=")
        left, right = value.replace("(", "").replace(")", "").split(",")
        maps[key].append(left)
        maps[key].append(right)

    steps = 0
    current = "AAA"
    while current != "ZZZ":
        for move in moves:
            current = maps[current][move]
            steps += 1
            if current == "ZZZ":
                break
    return steps


def all_end_with_z(arr):
    for s in arr:
        if not s.endswith("Z"):
            return False
    return True


def least_common_multiple(arr):
    return np.lcm.reduce(arr)


def part2(data):
    moves = list(map(lambda x: 0 if x == "L" else 1, data[0]))
    maps = defaultdict(list)
    currents = []
    for line in data[2:]:
        key, value = line.replace(" ", "").split("=")
        left, right = value.replace("(", "").replace(")", "").split(",")
        maps[key].append(left)
        maps[key].append(right)
        if key.endswith("A"):
            currents.append(key)

    steps_arr = []
    for current in currents:
        steps = 0
        initial = current
        while not initial.endswith("Z"):
            for move in moves:
                initial = maps[initial][move]
            steps += len(moves)
        steps_arr.append(steps)
    return least_common_multiple(steps_arr)


def part2_suboptimal(data):
    moves = list(map(lambda x: 0 if x == "L" else 1, data[0]))
    maps = defaultdict(list)
    currents = []
    for line in data[2:]:
        key, value = line.replace(" ", "").split("=")
        left, right = value.replace("(", "").replace(")", "").split(",")
        maps[key].append(left)
        maps[key].append(right)
        if key.endswith("A"):
            currents.append(key)

    steps_arr = []
    for current in currents:
        steps = 0
        has_seen = []
        initial = current
        br = False
        while not br:
            for idx, move in enumerate(moves):
                initial = maps[initial][move]
                if (initial, idx) in has_seen:
                    br = True
                    break
                has_seen.append((initial, idx))
                steps += 1
                if initial.endswith("Z"):
                    steps_arr.append(steps)
                    break
        print(steps_arr)
    return least_common_multiple(steps_arr)


def part2_bruteforce(data):
    moves = list(map(lambda x: 0 if x == "L" else 1, data[0]))
    maps = defaultdict(list)
    currents = []
    for line in data[2:]:
        key, value = line.replace(" ", "").split("=")
        left, right = value.replace("(", "").replace(")", "").split(",")
        maps[key].append(left)
        maps[key].append(right)
        if key.endswith("A"):
            currents.append(key)

    steps = 0
    while not all_end_with_z(currents):
        for move in moves:
            for i, current in enumerate(currents):
                currents[i] = maps[current][move]
            steps += 1
            if all_end_with_z(currents):
                break
    return steps


if __name__ == "__main__":
    # file = "2023/day_05/test.txt"
    # file = "test2.txt"
    # file = "2023/day_05/input.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
