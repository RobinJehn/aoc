import math
import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict

def expand_rows_map(plan,n):
    new_plan = []
    for line in plan:
        new_line = line[:]
        if "#" not in line:
            for _ in range(n-1):
                new_plan.append(new_line)
        new_plan.append(new_line)
    return new_plan

def expand_map(plan, n=2):
    new_plan = expand_rows_map(plan,n)
    transpose_plan = list(map(list, zip(*new_plan)))
    new_plan = expand_rows_map(transpose_plan,n)
    new_plan = list(map(list, zip(*new_plan)))
    return new_plan

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def total_pairwise_distance(points):
    total = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            # print(i, j, manhattan_distance(points[i], points[j]))
            total += manhattan_distance(points[i], points[j])
    return total

def get_points(plan):
    points = []
    for row_idx, line in enumerate(plan):
        for column_idx, char in enumerate(line):
            if char == "#":
                points.append((row_idx, column_idx))
    return points

def get_empty_rows(plan):
    rows = []
    for idx in range(len(plan)):
        if "#" not in plan[idx]:
            rows.append(idx)
    return rows

def get_empty_columns(plan):
    transpose_plan = list(map(list, zip(*plan)))
    columns = []
    for idx in range(len(transpose_plan)):
        if "#" not in transpose_plan[idx]:
            columns.append(idx)
    return columns

def special_manhattan_distance(a, b, empty_rows, empty_columns, n):
    dist = manhattan_distance(a, b)
    for i in range(min(a[0], b[0]), max(a[0], b[0])):
        if i in empty_rows:
            dist += n - 1
    for i in range(min(a[1], b[1]), max(a[1], b[1])):
        if i in empty_columns:
            dist += n - 1
    return dist

def total_special_pairwise_distance(points, empty_rows, empty_columns, n):
    total = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            total += special_manhattan_distance(points[i], points[j], empty_rows, empty_columns, n)
    return total

def part1(data):
    plan = expand_map(data)
    points = get_points(plan)
    return total_pairwise_distance(points)

def part2(data):
    plan = expand_map(data, 1)
    points = get_points(plan)
    empty_rows = get_empty_rows(plan)
    empty_columns = get_empty_columns(plan)
    return total_special_pairwise_distance(points, empty_rows, empty_columns, 100)


if __name__ == "__main__":
    # file = "2023/day_05/test.txt"
    file = "test.txt"
    # file = "2023/day_10/input.txt"
    # file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
