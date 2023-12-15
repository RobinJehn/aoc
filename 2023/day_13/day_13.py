import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache


def checkSymmetry(data, row):
    assert row >= 0 and row < len(data)
    pos = 0
    while row - pos - 1 >= 0 and row + pos < len(data):
        if data[row - pos - 1] != data[row + pos]:
            return False
        pos += 1
    return True


def checkSymmetrySmudge(data, row):
    assert row > 0 and row < len(data)
    pos = 0
    smudges = 0
    while row - pos - 1 >= 0 and row + pos < len(data) and smudges <= 1:
        smudges += rowCompare(data[row - pos - 1], data[row + pos])
        pos += 1
    return smudges == 1


def rowCompare(row1, row2):
    diff = 0
    for idx in range(len(row1)):
        if row1[idx] != row2[idx]:
            diff += 1
    return diff


def checkAllRowSymmetries(data):
    # print("\n".join(data))
    for idx in range(1, len(data)):
        if checkSymmetry(data, idx):
            return idx
    return None


def checkAllRowSymmetriesSmudge(data):
    # print("\n".join(data))
    for idx in range(1, len(data)):
        if checkSymmetrySmudge(data, idx):
            return idx
    return None


def checkAllSymetriesSmudge(data):
    row_idx = checkAllRowSymmetriesSmudge(data)
    column_idx = 0
    if row_idx is None:
        row_idx = 0
        column_idx = checkAllRowSymmetriesSmudge(
            list(map(lambda x: "".join(list(x)), zip(*data)))
        )
    return row_idx, column_idx


def checkAllSymetries(data):
    row_idx = checkAllRowSymmetries(data)
    column_idx = 0
    if row_idx is None:
        row_idx = 0
        column_idx = checkAllRowSymmetries(
            list(map(lambda x: "".join(list(x)), zip(*data)))
        )
    return row_idx, column_idx


def part1(data):
    total = 0
    data_array = []
    for line in data:
        if len(line.strip()) == 0:
            row_idx, column_idx = checkAllSymetries(data_array)
            # print(row_idx, column_idx)
            total += 100 * row_idx + column_idx
            data_array = []
            continue
        data_array.append(line)
    row_idx, column_idx = checkAllSymetries(data_array)
    total += 100 * row_idx + column_idx
    return total


def part2(data):
    total = 0
    data_array = []
    for line in data:
        if len(line.strip()) == 0:
            row_idx, column_idx = checkAllSymetriesSmudge(data_array)
            # print(row_idx, column_idx)
            total += 100 * row_idx + column_idx
            data_array = []
            continue
        data_array.append(line)
    row_idx, column_idx = checkAllSymetriesSmudge(data_array)
    total += 100 * row_idx + column_idx
    return total


if __name__ == "__main__":
    # file = "2023/day_12/input.txt"
    # file = "test.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
