import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache


def hash(string):
    value = 0
    for char in string:
        value += ord(char)
        value *= 17
        value %= 256
    return value


def part1(data):
    parts = data[0].split(",")
    return sum(list(map(hash, parts)))


def getLabel(string):
    if "-" in string:
        idx = string.find("-")
    else:
        idx = string.find("=")
    return string[:idx]


def part2(data):
    # idea: have a dict that stores (name, strength) for each box,
    lenses = {}
    parts = data[0].split(",")
    for part in parts:
        box = hash(getLabel(part))
        if box not in lenses:
            lenses[box] = []
        if "-" in part:
            idx = part.find("-")
            lenses[box] = list(filter(lambda x: x[0] != part[:idx], lenses[box]))
        else:
            idx = part.find("=")
            found = False
            for lens in lenses[box]:
                if lens[0] == part[:idx]:
                    lens[1] = int(part[idx + 1 :])
                    found = True
                    break
            if not found:
                lenses[box].append([part[:idx], int(part[idx + 1 :])])

    total = 0
    for key, lens_s in lenses.items():
        for idx, lens in enumerate(lens_s):
            total += (key + 1) * (idx + 1) * lens[1]
    return total


if __name__ == "__main__":
    # file = "2023/day_12/input.txt"
    # file = "test.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
