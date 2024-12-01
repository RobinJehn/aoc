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
import sys

sys.setrecursionlimit(1000)

np.set_printoptions(threshold=np.inf)


def toBrick(line):
    start, end = line.split("~")
    start = tuple(map(int, start.split(",")))
    end = tuple(map(int, end.split(",")))
    return start, end


def getMaxDims(bricks):
    max_x = 0
    max_y = 0
    max_z = 0
    for _, end, _ in bricks:
        max_x = max(max_x, end[0])
        max_y = max(max_y, end[1])
        max_z = max(max_z, end[2])

    return max_x + 1, max_y + 1, max_z + 1


def fall(grid, bricks):
    rests_on = {}
    supports = {}
    bricks.sort(key=lambda brick: brick[0][2])
    for start, end, letter in bricks:
        start_x, start_y, start_z = start
        end_x, end_y, end_z = end
        i = 1
        while (
            not (
                grid[
                    start_x : end_x + 1,
                    start_y : end_y + 1,
                    start_z - i,
                ]
                != 0
            ).any()
            and start_z - i > 0
        ):
            i += 1
        support = np.unique(
            grid[
                start_x : end_x + 1,
                start_y : end_y + 1,
                start_z - i,
            ]
        )
        support = np.delete(
            support,
            np.where(support == 0),
        )
        supports[letter] = set()
        rests_on[letter] = set(support)
        for brick in support:
            supports[brick].add(letter)
        i -= 1
        grid[
            start_x : end_x + 1, start_y : end_y + 1, start_z - i : end_z - i + 1
        ] = letter
    return rests_on, supports


def getBricksThatCanBeRemoved(supports, rests_on):
    can_be_removed = set()
    for brick, supportets in supports.items():
        remove = True
        for supported in supportets:
            if len(rests_on[supported]) == 1:
                remove = False
        if remove:
            can_be_removed.add(brick)
    return can_be_removed


def part1(data):
    bricks = []
    letter = 65  # A
    for line in data:
        start, end = toBrick(line)
        bricks.append((start, end, chr(letter)))
        letter += 1
    max_dims = getMaxDims(bricks)
    grid = np.full(max_dims, 0)
    rests_on, supports = fall(grid, bricks)
    can_be_removed = getBricksThatCanBeRemoved(supports, rests_on)
    return len(can_be_removed)


class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}

    def __call__(self, *args):
        rel_args = args[2:3]
        if not rel_args in self.memo:
            self.memo[rel_args] = self.f(*args)
        # Warning: You may wish to do a deepcopy here if returning objects
        return self.memo[rel_args]


def falls(supports, brick, f, rests_on):
    could_fall = supports[brick]
    new_falling = set()
    for pot_fall in could_fall:
        resting_on = copy.deepcopy(rests_on[pot_fall])
        resting_on.remove(brick)
        # We only fall if all we rest on falls
        if not resting_on.issubset(new_falling):
            continue
        new_falling.add(pot_fall)
        new_falling.update(f(supports, pot_fall, f, rests_on))
    return frozenset(new_falling)


def falls_correct(supports, rests_on, falling_bricks, mem_f):
    could_fall = set()
    for brick in falling_bricks:
        could_fall.update(supports[brick])

    new_falling = set()
    for pot_fall in could_fall:
        # We only fall if all we rest on falls
        things_we_rest_on = rests_on[pot_fall]
        if not things_we_rest_on.issubset(falling_bricks):
            continue
        new_falling.add(pot_fall)

    if len(new_falling) > 0:
        new_falling.update(mem_f(supports, rests_on, frozenset(new_falling), mem_f))
    return new_falling


def part2(data, falls=falls_correct):
    bricks = []
    letter = 0
    for line in data:
        start, end = toBrick(line)
        bricks.append((start, end, letter))
        letter += 1
    max_dims = getMaxDims(bricks)
    grid = np.full(max_dims, 0)
    rests_on, supports = fall(grid, bricks)
    can_be_removed = getBricksThatCanBeRemoved(supports, rests_on)

    falls = Memoize(falls)
    total = 0

    results = []
    bricks = sorted(bricks, key=lambda x: x[2])
    for _, _, brick in bricks:
        if brick in can_be_removed:
            continue
        would_fall = falls(supports, rests_on, frozenset([brick]), falls)
        results.append((brick, len(would_fall)))
        # print("brick", brick, len(would_fall))
        total += len(would_fall)
    results.sort(key=lambda x: x[0])
    for brick, count in results:
        print(brick, count)
    return total


if __name__ == "__main__":
    file = "2023/day_22/input.txt"
    # file = "test.txt"
    # file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        # print(part1(data))
        print(part2(data))
