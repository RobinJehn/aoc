from __future__ import annotations
import math

import numpy as np
from tqdm import tqdm
import re
from collections import Counter
from collections import defaultdict
import itertools
from functools import cache


def directionToIndex(direction):
    if direction == (1, 0):
        return 0
    elif direction == (-1, 0):
        return 1
    elif direction == (0, 1):
        return 2
    elif direction == (0, -1):
        return 3


class Node2:
    def __init__(self, index, direction, parent=None, g=math.inf, h=math.inf):
        self.index = index
        self.parent = parent
        self.direction = direction
        self.g = g
        self.h = h

    def __eq__(self, other):
        return (
            other != None
            and self.index == other.index
            and (
                self.direction == None
                or other.direction == None
                or self.direction == other.direction
            )
        )

    def __hash__(self):
        return hash((self.index, self.direction))

    def neighbors(self):
        count = None
        dir = None
        if self.direction != None:
            count = self.direction[0]
            dir = self.direction[1]

        if count != None and count < 4:
            return [
                Node2(
                    (self.index[0] + dir[0], self.index[1] + dir[1]),
                    (count + 1, dir),
                    self,
                )
            ]
        elif count == None:
            return [
                Node2(
                    (self.index[0] + 1, self.index[1] + 0),
                    (1, (1, 0)),
                    self,
                ),
                Node2(
                    (self.index[0], self.index[1] + 1),
                    (1, (0, 1)),
                    self,
                ),
            ]

        neighbors = []
        pos_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for new_dir in pos_dirs:
            if new_dir == dir:
                if count == 10:
                    continue
                else:
                    neighbors.append(
                        Node2(
                            (self.index[0] + dir[0], self.index[1] + dir[1]),
                            (count + 1, dir),
                            self,
                        )
                    )
                    continue
            if dir != None and new_dir == (-dir[0], -dir[1]):
                continue
            neighbors.append(
                Node2(
                    (self.index[0] + new_dir[0], self.index[1] + new_dir[1]),
                    (1, new_dir),
                    self,
                )
            )
        return neighbors


class Node:
    def __init__(self, index, direction, parent=None, g=math.inf, h=math.inf):
        self.index = index
        self.parent = parent
        self.direction = direction
        self.g = g
        self.h = h

    def __eq__(self, other):
        return (
            other != None
            and self.index == other.index
            and (
                self.direction == None
                or other.direction == None
                or self.direction == other.direction
            )
        )

    def __hash__(self):
        return hash((self.index, self.direction))

    def neighbors(self):
        count = None
        dir = None
        if self.direction != None:
            count = self.direction[0]
            dir = self.direction[1]

        neighbors = []
        pos_dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for new_dir in pos_dirs:
            if new_dir == dir:
                if count == 3:
                    continue
                else:
                    neighbors.append(
                        Node(
                            (self.index[0] + dir[0], self.index[1] + dir[1]),
                            (count + 1, dir),
                            self,
                        )
                    )
                    continue
            if dir != None and new_dir == (-dir[0], -dir[1]):
                continue
            neighbors.append(
                Node(
                    (self.index[0] + new_dir[0], self.index[1] + new_dir[1]),
                    (1, new_dir),
                    self,
                )
            )
        return neighbors


# Astar
def heuristic(node_a: Node, node_b: Node):
    index_a = node_a.index
    index_b = node_b.index
    return 1 * (abs(index_a[0] - index_b[0]) + abs(index_a[1] - index_b[1]))


def reconstructPath(cameFrom: dict[Node, Node], current: Node):
    total_path = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        total_path.append(current)
    return total_path


def astar(start: Node, goal: Node, costGrid):
    # The set of nodes already evaluated
    closedSet = set()
    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    openSet = set([start])
    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, cameFrom will eventually contain the
    # most efficient previous step.
    cameFrom = {}
    # For each node, the cost of getting from the start node to that node.
    gScore = defaultdict(lambda: math.inf)
    # The cost of going from start to start is zero.
    gScore[start] = 0
    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    fScore = defaultdict(lambda: math.inf)
    # For the first node, that value is completely heuristic.
    fScore[start] = heuristic(start, goal)

    while openSet:
        current = min(openSet, key=lambda x: fScore[x])
        print(len(closedSet), len(openSet), current.index)
        if current == goal:
            return reconstructPath(cameFrom, current)
        openSet.remove(current)
        closedSet.add(current)
        for neighbor in current.neighbors():
            n_idx = neighbor.index
            if (
                n_idx[0] < 0
                or n_idx[1] < 0
                or n_idx[0] >= len(costGrid)
                or n_idx[1] >= len(costGrid[0])
            ):
                continue
            if neighbor in closedSet:
                continue
            tentative_gScore = gScore[current] + costGrid[neighbor.index]
            if neighbor not in openSet:
                openSet.add(neighbor)
            elif tentative_gScore >= gScore[neighbor]:
                continue
            # This path is the best until now. Record it!
            cameFrom[neighbor] = current
            gScore[neighbor] = tentative_gScore
            neighbor.g = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + heuristic(neighbor, goal)
    return None


def part1(data):
    grid = np.array([[int(x) for x in line] for line in data])
    start = Node((0, 0), None)
    goal = Node((len(grid) - 1, len(grid[0]) - 1), None)
    path = astar(start, goal, grid)
    return path[0].g


def part2(data):
    grid = np.array([[int(x) for x in line] for line in data])
    start = Node2((0, 0), None)
    goal = Node2((len(grid) - 1, len(grid[0]) - 1), None)
    path = astar(start, goal, grid)
    return path[0].g


if __name__ == "__main__":
    # file = "2023/day_17/test.txt"
    # file = "test.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        # print(part1(data))
        print(part2(data))
