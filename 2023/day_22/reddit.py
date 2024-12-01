from collections import defaultdict


def dropped_brick(tallest, brick):
    peak = max(tallest[(x, y)] for x in range(brick[0], brick[3] + 1) for y in range(brick[1], brick[4] + 1))
    dz = max(brick[2] - peak - 1, 0)
    return (brick[0], brick[1], brick[2] - dz, brick[3], brick[4], brick[5] - dz)

def drop(tower):
    tallest = defaultdict(int)
    new_tower = []
    falls = 0
    for brick in tower:
        new_brick = dropped_brick(tallest, brick)
        if new_brick[2] != brick[2]:
            falls += 1
        new_tower.append(new_brick)
        for x in range(brick[0], brick[3] + 1):
            for y in range(brick[1], brick[4] + 1):
                tallest[(x, y)] = new_brick[5]
    return falls, new_tower

def ints(line):
    start, end = line.split("~")
    start = tuple(map(int, start.split(",")))
    end = tuple(map(int, end.split(",")))
    return start + end

def solve(data):
    bricks = sorted([ints(line) for line in data], key=lambda brick: brick[2])
    _, fallen = drop(bricks)
    p1 = p2 = 0
    for i in range(len(fallen)):
        removed = fallen[:i] + fallen[i + 1:]
        falls, _ = drop(removed)
        if not falls:
            p1 += 1
        else:
            p2 += falls
    return p1, p2

if __name__ == "__main__":
    data = open("input.txt").read().splitlines()
    print(solve(data))