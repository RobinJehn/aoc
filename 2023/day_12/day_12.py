import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache

def checkNumberCouldFit(number, text_part):
    counter = Counter(text_part)
    return number <= counter["#"] + counter["?"]


def checkOk(numbers, indices, text):
    for idx in range(len(indices) - 1):
        new_idx = numbers[idx] + indices[idx]
        if new_idx >= indices[idx + 1]:
            return False
        if len(text) > new_idx and text[new_idx] == "#":
            return False
    idx = len(indices) - 1
    new_idx = numbers[idx] + indices[idx]
    return "#" not in text[new_idx:]


def getNumberPossibilities(numbers, orig_text):
    possibilities = []
    for number in numbers:
        posses = getPossibilities(number, orig_text)
        possibilities.append(posses)
    count = 0
    for possibility in list(itertools.product(*possibilities)):
        if checkOk(numbers, possibility, orig_text):
            count += 1
    return count


def getPossibilities(number, text):
    possibilities = []
    for idx in range(len(text)):
        if '#' in text[:idx]:
            break
        if (
            checkNumberCouldFit(number, text[idx : idx + number])
            and (len(text) == idx + number or text[idx + number] != "#")
            and (idx - 1 < 0 or text[idx - 1] != "#")
        ):
            possibilities.append(idx)
    return possibilities

#Custom Decorator function
def listToTuple(function):
    def wrapper(*args):
        args = [tuple(x) if type(x) == list else x for x in args]
        result = function(*args)
        result = tuple(result) if type(result) == list else result
        return result
    return wrapper

#your cached function
@listToTuple
@cache
def recursiveNumberOfArangments(text, numbers):
    if len(numbers) == 0:
        return int("#" not in text)

    possibilities = getPossibilities(numbers[0], text)

    adding = 0
    for possibility in possibilities:
        if len(text) == possibility + numbers[0] and len(numbers) == 1:
            return adding + 1

        adding += recursiveNumberOfArangments(
            text[possibility + numbers[0] + 1 :], numbers[1:]
        )
    return adding


def part1(data):
    results = []
    for line in tqdm(data):
        orig_text, numbers = line.split(" ")
        numbers = [int(x) for x in numbers.split(",")]
        n = recursiveNumberOfArangments(orig_text, numbers)
        results.append(n)
    return sum(results)


def part2(data):
    results = []
    for line in tqdm(data):
        orig_text, numbers = line.split(" ")
        orig_text_long = orig_text
        for _ in range(4):
            orig_text_long += "?" + orig_text
        numbers = [int(x) for x in numbers.split(",")] * 5
        n = recursiveNumberOfArangments(orig_text_long, numbers)
        results.append(n)
    return sum(results)


if __name__ == "__main__":
    # file = "2023/day_12/input.txt"
    # file = "test.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        # print(part1(data))
        print(part2(data))
