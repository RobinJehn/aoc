import math
import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict


def get_deriv(arr):
    if len(arr) == 0:
        return [0]
    deriv = []
    for i in range(len(arr) - 1):
        deriv.append(arr[i + 1] - arr[i])
    return deriv


def add_derivs(arr):
    deriv = get_deriv(arr)
    if all([v == 0 for v in deriv]):
        arr.append(arr[-1])
        return arr
    else:
        deriv = add_derivs(deriv)
        arr.append(arr[-1] + deriv[-1])
        return arr


def add_derivs2(arr):
    deriv = get_deriv(arr)
    if all([v == 0 for v in deriv]):
        arr = [arr[0]] + arr
        return arr
    else:
        deriv = add_derivs2(deriv)
        arr = [arr[0]- deriv[0]] + arr
        return arr

def part1(data):
    total = 0
    for line in data:
        values = [int(x) for x in line.split()]
        new_values = add_derivs(values)
        total += new_values[-1]

    return total 


def part2(data):
    total = 0
    for line in data:
        values = [int(x) for x in line.split()]
        new_values = add_derivs2(values)
        total += new_values[0]

    return total 


if __name__ == "__main__":
    # file = "2023/day_05/test.txt"
    # file = "test2.txt"
    # file = "2023/day_05/input.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
