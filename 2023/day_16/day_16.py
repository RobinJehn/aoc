import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache


def newDirections(direction, char):
    if char == "/":
        if direction == (1, 0):
            return [(0, -1)]
        elif direction == (-1, 0):
            return [(0, 1)]
        elif direction == (0, 1):
            return [(-1, 0)]
        elif direction == (0, -1):
            return [(1, 0)]
    elif char == "\\":
        if direction == (1, 0):
            return [(0, 1)]
        elif direction == (-1, 0):
            return [(0, -1)]
        elif direction == (0, 1):
            return [(1, 0)]
        elif direction == (0, -1):
            return [(-1, 0)]
    elif char == "|":
        if direction == (0, 1) or direction == (0, -1):
            return [(1, 0), (-1, 0)]
        else:
            return direction
    elif char == "-":
        if direction == (1, 0) or direction == (-1, 0):
            return [(0, 1), (0, -1)]
        else:
            return direction
    else:
        return direction


def directionToIndex(direction):
    if direction == (1, 0):
        return 0
    elif direction == (-1, 0):
        return 1
    elif direction == (0, 1):
        return 2
    elif direction == (0, -1):
        return 3


def array2dToTupleTuple(array):
    return tuple(tuple(l) for l in array)

def array3dToTuple(array):
    return tuple(tuple(tuple(j) for j in l) for l in array)

def tuple2dToList(tuple):
    l = []
    for sub_tuple in tuple:
        new_sub_l = []
        for element in sub_tuple:
            new_sub_l.append(element)
        l.append(new_sub_l)
    return l

def tuple3dToList(tuple):
    l = []
    for sub_tuple in tuple:
        new_sub_l = []
        for sub_sub_tuple in sub_tuple:
            new_sub_sub_l = []
            for element in sub_sub_tuple:
                new_sub_sub_l.append(element)
            new_sub_l.append(new_sub_sub_l)
        l.append(new_sub_l)
    return np.array(l)


# Doesn't memoze the moves I do inside moveRay, only memorizes splits
class Memoize:
    def __init__(self, f):
        self.f = f
        self.memo = {}
    def __call__(self, *args):
        rel_args = args[:3]
        if not rel_args in self.memo:
            self.memo[rel_args] = self.f(*args)
        #Warning: You may wish to do a deepcopy here if returning objects
        return self.memo[rel_args]

def moveRay(grid, idx, direction, seen):
    row_idx = idx[0] + direction[0]
    column_idx = idx[1] + direction[1]
    if (
        row_idx < 0
        or row_idx >= len(grid)
        or column_idx < 0
        or column_idx >= len(grid[0])
    ):
        return seen
    seen = tuple3dToList(seen)
    while not (
        row_idx < 0
        or row_idx >= len(grid)
        or column_idx < 0
        or column_idx >= len(grid[0])
        or seen[row_idx, column_idx, directionToIndex(direction)]
    ):
        seen[row_idx, column_idx, directionToIndex(direction)] = True

        char = grid[row_idx][column_idx]
        new_dirs = newDirections(direction, char)
        if new_dirs != direction:
            for newDirection in newDirections(direction, char):
                seen_t = moveRay(
                    grid, (row_idx, column_idx), newDirection, array3dToTuple(seen)
                )
                seen |= tuple3dToList(seen_t)
            break
        else:
            row_idx += direction[0]
            column_idx += direction[1]
    return array3dToTuple(seen)


def part1(data, moveRay):
    grid = np.array([list(line) for line in data])
    grid = array2dToTupleTuple(grid)
    seen = moveRay(
        grid,
        (0, -1),
        (0, 1),
        array3dToTuple(np.full((len(grid), len(grid[0]), 4), False)),
    )
    return np.sum(np.any(seen, axis=2))


def part2(data, moveRay):
    grid = np.array([list(line) for line in data])
    grid = array2dToTupleTuple(grid)
    found = []
    for i in tqdm(range(len(grid))):
        seen = moveRay(
            grid,
            (i, -1),
            (0, 1),
            array3dToTuple(np.full((len(grid), len(grid[0]), 4), False)),
        )
        found.append(np.sum(np.any(seen, axis=2)))
        seen = moveRay(
            grid,
            (i, len(grid[0])),
            (0, -1),
            array3dToTuple(np.full((len(grid), len(grid[0]), 4), False)),
        )
        found.append(np.sum(np.any(seen, axis=2)))
    for i in tqdm(range(len(grid[0]))):
        seen = moveRay(
            grid,
            (-1, i),
            (1, 0),
            array3dToTuple(np.full((len(grid), len(grid[0]), 4), False)),
        )
        found.append(np.sum(np.any(seen, axis=2)))
        seen = moveRay(
            grid,
            (len(grid), i),
            (-1, 0),
            array3dToTuple(np.full((len(grid), len(grid[0]), 4), False)),
        )
        found.append(np.sum(np.any(seen, axis=2)))
    return np.max(found)


if __name__ == "__main__":
    # file = "2023/day_16/test.txt"
    file = "test.txt"
    # file = "input.txt"
    moveRay = Memoize(moveRay)
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data, moveRay))
        print(part2(data, moveRay))
