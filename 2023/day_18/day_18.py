from __future__ import annotations
import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache

np.set_printoptions(threshold=np.inf)


def locations(moves):
    positions = [(0, 0)]
    current_row = 0
    current_col = 0
    for direction, amount in moves:
        if direction == "R":
            current_col += amount
        elif direction == "U":
            current_row -= amount
        elif direction == "D":
            current_row += amount
        elif direction == "L":
            current_col -= amount
        positions.append((current_row, current_col))
    return positions


def max_extension(moves):
    current_row = 0
    current_col = 0
    max_row = 0
    max_col = 0
    min_row = 0
    min_col = 0
    for direction, amount in moves:
        if direction == "R":
            current_col += amount
        elif direction == "U":
            current_row -= amount
        elif direction == "D":
            current_row += amount
        elif direction == "L":
            current_col -= amount
        max_row = max(max_row, current_row)
        max_col = max(max_col, current_col)
        min_row = min(min_row, current_row)
        min_col = min(min_col, current_col)
    return min_row, min_col, max_row, max_col


def dig(grid, moves, start_pos):
    current_row, current_col = start_pos
    for direction, amount in moves:
        if direction == "R":
            grid[current_row, current_col : current_col + amount] = "#"
            current_col += amount
        elif direction == "U":
            grid[current_row - amount : current_row + 1, current_col] = "#"
            current_row -= amount
        elif direction == "D":
            grid[current_row : current_row + amount, current_col] = "#"
            current_row += amount
        elif direction == "L":
            grid[current_row, current_col - amount : current_col + 1] = "#"
            current_col -= amount
    return grid


def connect_neighbours(data, row_idx, column_idx, new_val):
    new_posses = []
    for i, j in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        if (
            len(data) <= row_idx + i
            or row_idx + i < 0
            or len(data[0]) <= column_idx + j
            or column_idx + j < 0
        ):
            continue
        if data[row_idx + i][column_idx + j] == ".":
            data[row_idx + i][column_idx + j] = new_val
            new_posses.append((row_idx + i, column_idx + j))
    return new_posses


def flood_fill(data, new_char="O"):
    new_posses = []
    for i in range(len(data)):
        if data[i, 0] == ".":
            data[i, 0] = new_char
            new_posses += connect_neighbours(data, i, 0, new_char)
        if data[i, len(data[0]) - 1] == ".":
            data[i, len(data[0]) - 1] = new_char
            new_posses += connect_neighbours(data, i, len(data[0]) - 1, new_char)
    for j in range(len(data[0])):
        if data[0, j] == ".":
            data[0, j] = new_char
            new_posses += connect_neighbours(data, 0, j, new_char)
        if data[len(data) - 1, j] == ".":
            data[len(data) - 1, j] = new_char
            new_posses += connect_neighbours(data, len(data) - 1, j, new_char)

    while new_posses != []:
        new_new_posses = []
        for pos in new_posses:
            if data[pos[0], pos[1]] == new_char:
                new_new_posses += connect_neighbours(data, pos[0], pos[1], new_char)
        new_posses = new_new_posses


def extract_move(colour: str):
    colour = colour.replace("(", "").replace(")", "").replace("#", "")
    num = int(colour[:5], 16)
    move = int(colour[5])
    if move == 0:
        return "R", num
    elif move == 1:
        return "D", num
    elif move == 2:
        return "L", num
    elif move == 3:
        return "U", num


def shoelace(points):
    n = len(points)
    return 0.5 * abs(
        sum(
            [
                points[i][0] * points[(i + 1) % n][1]
                - points[(i + 1) % n][0] * points[i][1]
                for i in range(n)
            ]
        )
    )


def part1(data):
    moves = []
    for line in data:
        direction, amount, colour = line.split(" ")
        moves.append((direction, int(amount)))
    min_row, min_col, max_row, max_col = max_extension(moves)

    grid = np.full((max_row - min_row + 1, max_col - min_col + 1), ".")
    start_pos = (0 - min_row, 0 - min_col)
    grid = dig(grid, moves, start_pos)
    # for line in grid:
    #     print("".join(line))
    flood_fill(grid)
    counter = Counter(grid.flatten())
    return grid.size - counter["O"]


def part2(data):
    moves = []
    for line in data:
        direction, amount, colour = line.split(" ")
        direction, amount = extract_move(colour)
        moves.append((direction, int(amount)))
    points = locations(moves)
    shoelace(points)
    return int(shoelace(points) + sum(amount for _, amount in moves) / 2 + 1)
    # min_row, min_col, max_row, max_col = max_extension(moves)

    # grid = np.full((max_row - min_row + 1, max_col - min_col + 1), ".")
    # start_pos = (0 - min_row, 0 - min_col)
    # grid = dig(grid, moves, start_pos)
    # flood_fill(grid)
    # counter = Counter(grid.flatten())
    # return grid.size - counter["O"]


if __name__ == "__main__":
    # file = "2023/day_17/test.txt"
    # file = "test.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        # print(part1(data))
        print(part2(data))
