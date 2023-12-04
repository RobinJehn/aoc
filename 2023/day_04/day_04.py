import math
def to_numbers(string):
    return [int(x) for x in string.split(" ") if x != ""]

def part1(data):
    game_value = []
    for line in data:
        _, game_str = line.split(":")
        win_str, your_str = game_str.split("|")
        winning_numbers = to_numbers(win_str)
        yours_numbers = to_numbers(your_str)
        count = 0
        for your_number in yours_numbers:
            if your_number in winning_numbers:
                count += 1
        val = 0
        if count != 0:
            val = int(math.pow(2, count -1))
        game_value.append(val)
    return sum(game_value)

def part2(data):
    total_cards = 0
    cards_in_queue = []
    for line in data:
        id_str, game_str = line.split(":")
        id = int(id_str[5:])
        win_str, your_str = game_str.split("|")
        winning_numbers = to_numbers(win_str)
        yours_numbers = to_numbers(your_str)
        count = 0
        for your_number in yours_numbers:
            if your_number in winning_numbers:
                count += 1
        total_cards += 1
        for _ in range(cards_in_queue.count(id) + 1):
            for i in range(count):
                cards_in_queue.append(id + i + 1)
                total_cards += 1
    return total_cards

if __name__ == "__main__":
    file = "input.txt"
    with open(file) as f:
        data = f.read().splitlines()
        print(part1(data))
        print(part2(data))
