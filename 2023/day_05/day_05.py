import math
import numpy as np


def part1(data):
    values = []
    maps = {}
    for line in data:
        if line.startswith("seeds:"):
            seeds_str = line.split(":")[1].split()
            seeds = [int(s) for s in seeds_str]
            continue
        if len(line) == 0:
            continue
        if line[0].isalpha():
            map_name = line.split(":")[0]
            maps[map_name] = []
            continue
        if line[0].isdigit():
            numbers_str = line.split()
            numbers = [int(n) for n in numbers_str]
            maps[map_name].append(numbers)

    current_map = "seed"
    for seed in seeds:
        value = seed
        cond = True
        while cond:
            for map_name, map_values in maps.items():
                if map_name.startswith(current_map):
                    current_map = map_name.split()[0].split("-")[2]
                    for dest_range, start_range, range in map_values:
                        if start_range <= value <= start_range + range - 1:
                            value = dest_range + value - start_range
                            break
                    if current_map.endswith("location"):
                        values.append(value)
                        current_map = "seed"
                        cond = False
                        break
    return min(values)


def do_overlap(a, b):
    if a[0] <= b[0] <= a[0] + a[1] - 1:  # b starts in a
        return True
    if b[0] <= a[0] <= b[0] + b[1] - 1:  # a starts in b
        return True
    return False


def overlap(a, b):
    return (
        max(a[0], b[0]),
        min(a[0] + a[1], b[0] + b[1]) - max(a[0], b[0]),
    )


def no_overlap(a, b):
    # b wird gesplittet
    ov = overlap(a, b)
    if ov == b:
        return None
    if ov[0] <= b[0]:  # Start ist gleich oder ov startet vor b
        return [(ov[0] + ov[1], (b[0] + b[1]) - (ov[0] + ov[1]))]
    if ov[0] + ov[1] - 1 >= b[0] + b[1] - 1:  # Ende ist gleich oder ov endet nach b
        return [(b[0], ov[0] - b[0])]
    return [(b[0], ov[0] - b[0]), (ov[0] + ov[1], (b[0] + b[1]) - (ov[0] + ov[1]))]


def part2(data):
    values = []
    maps = {}
    for line in data:
        if len(line) == 0:
            continue

        if line.startswith("seeds:"):
            seeds_str = line.split(":")[1].split()
            seeds_pairs = [int(s) for s in seeds_str]
            seeds = []
            for idx in range(0, len(seeds_pairs), 2):
                seeds.append([seeds_pairs[idx], seeds_pairs[idx + 1]])
            continue

        if line[0].isalpha():
            map_name = line.split(":")[0]
            maps[map_name] = []
            continue

        if line[0].isdigit():
            numbers_str = line.split()
            numbers = [int(n) for n in numbers_str]
            maps[map_name].append(numbers)
            continue

    current_map = "seed"
    for seed_start, seed_range in seeds:
        value = [(seed_start, seed_range)]
        for map_name, map_values in maps.items():
            new_value = []
            current_map = map_name.split()[0].split("-")[2]
            for seed_sta, seed_ran in value:
                not_covered = [(seed_sta, seed_ran)]
                for dest_range, start_range, range_v in map_values:
                    ## If applies to part of range apply to that range
                    if do_overlap((start_range, range_v), (seed_sta, seed_ran)):
                        ov = overlap(
                            (start_range, range_v),
                            (seed_sta, seed_ran),
                        )
                        new_not_covered = not_covered[:]
                        for sta, ran in not_covered:
                            if do_overlap(ov, (sta, ran)):
                                new_not_covered.remove((sta, ran))
                                no_ov = no_overlap(ov, (sta, ran))
                                if no_ov == None:
                                    continue
                                if len(no_ov) == 1:
                                    new_not_covered.append(no_ov[0])
                                else:
                                    new_not_covered.append(no_ov[0])
                                    new_not_covered.append(no_ov[1])
                        not_covered = new_not_covered[:]
                        new_value.append((ov[0] + dest_range - start_range, ov[1]))
                for sta, ran in not_covered:
                    new_value.append((sta, ran))
            value = new_value
            if current_map.endswith("location"):
                values.append(min(value, key=lambda x: x[0]))
                current_map = "seed"
                break
    return min(values)[0]


if __name__ == "__main__":
    # file = "2023/day_05/test.txt"
    # file = "test.txt"
    # file = "2023/day_05/input.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
