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
from enum import Enum

np.set_printoptions(threshold=np.inf)

def expand(garden, position):
    new_postions = []
    row, col = position
    if row > 0 and garden[row - 1, col] != "#":
        new_postions.append((row - 1, col))
    if row < len(garden) - 1 and garden[row + 1, col] != "#":
        new_postions.append((row + 1, col))
    if col > 0 and garden[row, col - 1] != "#":
        new_postions.append((row, col - 1))
    if col < len(garden[0]) - 1 and garden[row, col + 1] != "#":
        new_postions.append((row, col + 1))
    return new_postions

def walk(garden, starting_row, starting_col, steps = 64):
    positions = [(starting_row, starting_col)]
    for _ in range(steps):
        new_postions = set()
        for position in positions:
            new_postions.update(expand(garden, position))
        positions = new_postions
    return positions

def part1(data):
    garden = np.array([list(line) for line in data])
    starting_pos = np.where(garden == "S")
    starting_row = starting_pos[0][0]
    starting_col = starting_pos[1][0]
    return len(walk(garden, starting_row, starting_col))

def part2(data):
   pass


if __name__ == "__main__":
    # file = "2023/day_20/test2.txt"
    # file = "test.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
