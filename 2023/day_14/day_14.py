import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache


def goThroughColumn(data, column_idx):
    value = 0
    max_value = len(data)
    for row_idx in range(len(data)):
        if data[row_idx][column_idx] == "O":
            value += max_value
            max_value -= 1
        if data[row_idx][column_idx] == "#":
            max_value = len(data) - row_idx - 1

    return value


# Custom Decorator function
def array2dToTupleTuple(array):
    return tuple(tuple(l) for l in array)


def listLToTTuple(function):
    def wrapper(*args):
        args = array2dToTupleTuple(args[0])
        result = function(args)
        result = tuple(result) if type(result) == list else result
        return result

    return wrapper

def listToTuple(function):
    def wrapper(*args):
        args = [tuple(x) if type(x) == list else x for x in args]
        result = function(*args)
        result = tuple(result) if type(result) == list else result
        return result

    return wrapper


def tupleToList(tuple):
   return list(tuple)

def tuple2dToList(tuple):
    l = []
    for sub_tuple in tuple:
        new_sub_l = []
        for element in sub_tuple:
            new_sub_l.append(element)
        l.append(new_sub_l)
    return l

def tuple2dTonp(tuple):
    return np.array(tuple2dToList(tuple))

def columnToRow(column):
    return tuple(zip(*column))


def rowToColumn(row):
    return row.T


@cache
def rollRight(row):
    row = tupleToList(row)
    max_value = len(row) - 1
    for inv_idx in range(len(row)):
        col_idx = len(row) - 1 - inv_idx
        if row[col_idx] == "O":
            row[col_idx] = "."
            row[max_value] = "O"
            max_value -= 1

        if row[col_idx] == "#":
            max_value = col_idx - 1
    return np.array([row])


@cache
def rollLeft(row):
    row = tupleToList(row)
    min_value = 0
    for col_idx in range(len(row)):
        if row[col_idx] == "O":
            row[col_idx] = "."
            row[min_value] = "O"
            min_value += 1

        if row[col_idx] == "#":
            min_value = col_idx + 1
    return np.array([row])


@listToTuple
@cache
def rollUp(column):
    return rowToColumn(rollLeft(columnToRow(column)[0]))


@listToTuple
@cache
def rollDown(column):
    return rowToColumn(rollRight(columnToRow(column)[0]))


def part1(data):
    total = 0
    data_array = []
    for line in data:
        data_array.append(line)
    for column_idx in range(len(data_array[0])):
        total += goThroughColumn(data_array, column_idx)
    return total

@listLToTTuple
@cache
def m(data_array):
    data_array = tuple2dTonp(data_array)
    for column_idx in range(len(data_array[0])):
        data_array[:, [column_idx]] = rollUp(array2dToTupleTuple(data_array[:, column_idx]))
    for row_idx in range(len(data_array)):
        data_array[row_idx, :] = rollLeft(tuple(data_array[row_idx, :]))[0]
    for column_idx in range(len(data_array[0])):
        data_array[:, [column_idx]] = rollDown(array2dToTupleTuple(data_array[:, column_idx]))
    for row_idx in range(len(data_array)):
        data_array[[row_idx], :] = rollRight(tuple(data_array[row_idx, :]))[0]
    return data_array

def part2(data):
    data_array = np.full((len(data), len(data[0])), "")
    for row_idx, line in enumerate(data):
        for column_idx, char in enumerate(line):
            data_array[row_idx, column_idx] = char

    seen_positions = {}
    d_array_tuple = array2dToTupleTuple(data_array)
    i = 0
    while True:
        seen_positions[d_array_tuple] = i
        data_array = m(data_array)
        d_array_tuple = array2dToTupleTuple(data_array)
        i += 1
        if d_array_tuple in seen_positions:
            break
    
    cycle_length = i - seen_positions[d_array_tuple]
    cycles = 1000000000 - i
    repetitions = cycles // cycle_length
    remaining = cycles - repetitions * cycle_length
    # print(cycle_length, i, repetitions, remaining)

    for i in range(remaining):
        data_array = m(data_array)


    for line in data_array:
        print("".join(line))

    total = 0
    for row_idx in range(len(data_array)):
        for column_idx in range(len(data_array[0])):
            if data_array[row_idx, column_idx] == 'O':
                total += len(data_array[0]) - row_idx
    return total


if __name__ == "__main__":
    # file = "2023/day_12/input.txt"
    # file = "test.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
