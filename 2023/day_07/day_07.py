import math
import numpy as np
from tqdm import tqdm
import re
from collections import Counter


def rank_2(char):
    if char.isdigit():
        return int(char) - 1
    elif char == "T":
        return 9
    elif char == "J":
        return 0
    elif char == "Q":
        return 10
    elif char == "K":
        return 11
    elif char == "A":
        return 12


def hand_rank_2(hand):
    return (
        math.pow(13, 4) * rank_2(hand[0])
        + math.pow(13, 3) * rank_2(hand[1])
        + math.pow(13, 2) * rank_2(hand[2])
        + math.pow(13, 1) * rank_2(hand[3])
        + math.pow(13, 0) * rank_2(hand[4])
    )


def rank(char):
    if char.isdigit():
        return int(char) - 2
    elif char == "T":
        return 8
    elif char == "J":
        return 9
    elif char == "Q":
        return 10
    elif char == "K":
        return 11
    elif char == "A":
        return 12


def hand_rank(hand):
    return (
        math.pow(13, 4) * rank(hand[0])
        + math.pow(13, 3) * rank(hand[1])
        + math.pow(13, 2) * rank(hand[2])
        + math.pow(13, 1) * rank(hand[3])
        + math.pow(13, 0) * rank(hand[4])
    )


def score_1(hand):
    counts = Counter(hand)
    counts_vals = list(counts.values())
    if 5 in counts_vals:
        return math.pow(13, 5) * 6 + hand_rank(hand)
    if 4 in counts_vals:
        return math.pow(13, 5) * 5 + hand_rank(hand)
    if 3 in counts_vals and 2 in counts_vals:
        return math.pow(13, 5) * 4 + hand_rank(hand)
    if 3 in counts_vals:
        return math.pow(13, 5) * 3 + hand_rank(hand)
    if counts_vals.count(2) == 2:
        return math.pow(13, 5) * 2 + hand_rank(hand)
    if 2 in counts_vals:
        return math.pow(13, 5) * 1 + hand_rank(hand)
    return hand_rank(hand)


def score_2(hand):
    hand_f = hand
    if "J" in hand:
        counts_j = Counter(hand)
        m_c = counts_j.most_common(1)[0]
        if m_c[0] == "J" and m_c[1] != 5:
            m_c = counts_j.most_common(2)[1]
        hand_f = hand.replace("J", m_c[0])

    counts = Counter(hand_f)
    counts_vals = list(counts.values())
    if 5 in counts_vals:
        return math.pow(13, 5) * 6 + hand_rank_2(hand)
    if 4 in counts_vals:
        return math.pow(13, 5) * 5 + hand_rank_2(hand)
    if 3 in counts_vals and 2 in counts_vals:
        return math.pow(13, 5) * 4 + hand_rank_2(hand)
    if 3 in counts_vals:
        return math.pow(13, 5) * 3 + hand_rank_2(hand)
    if counts_vals.count(2) == 2:
        return math.pow(13, 5) * 2 + hand_rank_2(hand)
    if 2 in counts_vals:
        return math.pow(13, 5) * 1 + hand_rank_2(hand)
    return hand_rank_2(hand)


def part1(data):
    hands = []
    for line in data:
        hand, bid = line.split()
        hands.append((hand, int(bid)))

    sorted_hands = sorted(hands, key=lambda x: score_1(x[0]))
    total = 0
    for idx, (hand, bid) in enumerate(sorted_hands):
        total += bid * (idx + 1)
    return total


def part2(data):
    hands = []
    for line in data:
        hand, bid = line.split()
        hands.append((hand, int(bid)))

    sorted_hands = sorted(hands, key=lambda x: score_2(x[0]))
    total = 0
    for idx, (hand, bid) in enumerate(sorted_hands):
        total += bid * (idx + 1)
    return total


if __name__ == "__main__":
    # file = "2023/day_05/test.txt"
    # file = "test.txt"
    # file = "2023/day_05/input.txt"
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
