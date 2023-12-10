import math
# import numpy as np
# from tqdm import tqdm
# import re
from collections import Counter
from collections import defaultdict


def to_indices(pipe):
    if pipe == "-":
        return [(0, 1), (0, -1)]
    elif pipe == "|":
        return [(-1, 0), (1, 0)]
    elif pipe == "L":
        return [(-1, 0), (0, 1)]
    elif pipe == "J":
        return [(-1, 0), (0, -1)]
    elif pipe == "7":
        return [(1, 0), (0, -1)]
    elif pipe == "F":
        return [(1, 0), (0, 1)]
    else:
        return []


def to_pipe(to_indices):
    to_indices = sorted(to_indices)
    if to_indices == sorted([(0, 1), (0, -1)]):
        return "-"
    elif to_indices == sorted([(1, 0), (-1, 0)]):
        return "|"
    elif to_indices == sorted([(-1, 0), (0, 1)]):
        return "L"
    elif to_indices == sorted([(-1, 0), (0, -1)]):
        return "J"
    elif to_indices == sorted([(1, 0), (0, -1)]):
        return "7"
    elif to_indices == sorted([(1, 0), (0, 1)]):
        return "F"
    else:
        print("ERROR", to_indices)


def s_pipe(plan, row_idx, column_idx):
    positions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    connected_to = []
    for pos in positions:
        if len(plan) <= row_idx + pos[0] < 0 or len(plan[0]) <= column_idx + pos[1] < 0:
            continue
        conns = to_indices(plan[row_idx + pos[0]][column_idx + pos[1]])
        for conn in conns:
            if conn == (-pos[0], -pos[1]):
                connected_to.append(pos)

    return to_pipe(connected_to)


def part1(data):
    for row_idx, line in enumerate(data):
        for column_idx, char in enumerate(line):
            if char == "S":
                start_pos = (row_idx, column_idx)
                # data[row_idx][column_idx] = s_pipe(data, row_idx, column_idx)
                break

    cost = []
    cur_cost = 0
    current_pos = start_pos
    previous_con = None
    while len(cost) == 0 or data[current_pos[0]][current_pos[1]] != "S":
        cost.append((current_pos, cur_cost))
        cur_cost += 1
        if data[current_pos[0]][current_pos[1]] == "S":
            conns = to_indices(s_pipe(data, current_pos[0], current_pos[1]))
            conn = conns[0]
            previous_con = conn
            current_pos = (current_pos[0] + conn[0], current_pos[1] + conn[1])
            continue
        conns = to_indices(data[current_pos[0]][current_pos[1]])
        for conn in conns:
            if conn != (-previous_con[0], -previous_con[1]):
                previous_con = conn
                current_pos = (current_pos[0] + conn[0], current_pos[1] + conn[1])
                break
    return len(cost) // 2


def show_map(data):
    for line in data:
        print("".join(line))


def only_keep_loop(data):
    new_data = [["." for _ in line] for line in data]
    for row_idx, line in enumerate(data):
        for column_idx, char in enumerate(line):
            if char == "S":
                start_pos = (row_idx, column_idx)
                break

    current_pos = start_pos
    previous_con = None
    while previous_con == None or data[current_pos[0]][current_pos[1]] != "S":
        if data[current_pos[0]][current_pos[1]] == "S":
            pipe = s_pipe(data, current_pos[0], current_pos[1])
            new_data[current_pos[0]][current_pos[1]] = pipe
            conns = to_indices(pipe)
            conn = conns[0]
            previous_con = conn
            current_pos = (current_pos[0] + conn[0], current_pos[1] + conn[1])
            new_data[current_pos[0]][current_pos[1]] = data[current_pos[0]][
                current_pos[1]
            ]
            continue
        conns = to_indices(data[current_pos[0]][current_pos[1]])
        for conn in conns:
            if conn != (-previous_con[0], -previous_con[1]):
                previous_con = conn
                current_pos = (current_pos[0] + conn[0], current_pos[1] + conn[1])
                if data[current_pos[0]][current_pos[1]] != "S":
                    new_data[current_pos[0]][current_pos[1]] = data[current_pos[0]][
                        current_pos[1]
                    ]
                break
    return new_data, start_pos


def make_bigger(data):
    new_data = [["." for _ in range(2 * len(data[0]))] for _ in range(2 * len(data))]
    for row_idx, line in enumerate(data):
        for column_idx, char in enumerate(line):
            new_data[2 * row_idx][2 * column_idx] = char
            if char == ".":
                continue
            indices = to_indices(char)
            for idx in indices:
                if idx[0] == 0:
                    new_char = "-"
                else:
                    new_char = "|"
                new_data[2 * row_idx + idx[0]][2 * column_idx + idx[1]] = new_char

    return new_data


def connect_neighbours(data, row_idx, column_idx, new_char):
    new_posses = []
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue
            if (
                len(data) <= row_idx + i - 1 or row_idx + i - 1 < 0
                or len(data[0]) <= column_idx + j - 1 or column_idx + j - 1 < 0
            ):
                continue
            if data[row_idx + i - 1][column_idx + j - 1] == ".":
                data[row_idx + i - 1][column_idx + j - 1] = new_char
                new_posses.append((row_idx + i - 1, column_idx + j - 1))
    return new_posses


def make_smaller(data):
    new_data = [["." for _ in range(len(data[0]) // 2)] for _ in range(len(data) // 2)]
    for row_idx in range(0, len(data), 2):
        for column_idx in range(0, len(data[0]), 2):
            if data[row_idx][column_idx] == ".":
                continue
            new_data[row_idx // 2][column_idx // 2] = data[row_idx][column_idx]
    return new_data


def flood_fill(data):
    new_posses = []
    for i in range(len(data)):
        new_posses += connect_neighbours(data, i, 0, "X")
        new_posses += connect_neighbours(data, i, len(data[0]) - 1, "X")
    for j in range(len(data[0])):
        new_posses += connect_neighbours(data, 0, j, "X")
        new_posses += connect_neighbours(data, len(data[0]) - 1, j, "X")

    while new_posses != []:
        new_new_posses = []
        for pos in new_posses:
            new_new_posses += connect_neighbours(
                data, pos[0], pos[1], "X"
            )
        new_posses = new_new_posses


def part2(data):
    loop, _ = only_keep_loop(data)
    bigger_loop = make_bigger(loop)
    flood_fill(bigger_loop)
    orig_loop = make_smaller(bigger_loop)
    # show_map(orig_loop)

    total_string = ""
    for line in orig_loop:
        total_string += "".join(line)
    new_count = Counter(total_string)
    return new_count['.']


if __name__ == "__main__":
    # file = "2023/day_05/test.txt"
    # file = "test.txt"
    # file = "2023/day_10/input.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
