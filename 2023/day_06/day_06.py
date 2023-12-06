import math
import numpy as np
from tqdm import tqdm


def part1(data):
    for line in data:
        if line.startswith("Time"):
            times = line.split(":")[1].split()
            times = [int(num) for num in times]
        else:
            distances = line.split(":")[1].split()
            distances = [int(num) for num in distances]
    values = []
    for idx, time in enumerate(times):
        sub_values = []
        for time_v in range(time):
            if time_v * (time - time_v) > distances[idx]:
                sub_values.append(time_v)
        values.append(len(sub_values))
    return np.prod(values)


def part2(data):
    for line in data:
        if line.startswith("Time"):
            time = line.split(":")[1].replace(" ", "")
            time = int(time)
        else:
            distance = line.split(":")[1].replace(" ", "")
            distance = int(distance)
    values = []
    for time_v in range(time):
        if time_v * (time - time_v) > distance:
            values.append(time_v)
    return len(values)


if __name__ == "__main__":
    # file = "2023/day_05/test.txt"
    # file = "test.txt"
    # file = "2023/day_05/input.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
