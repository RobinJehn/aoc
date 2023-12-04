def part1(data):
    nums = []
    for line in data.splitlines():
        first = None
        last = None
        for char in line:
            if char.isdigit():
                if first is None:
                    first = char
                last = char
        nums.append(int(first + last))
    return sum(nums)

def part2(data):
    nums = []
    to_digit = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    for line in data.splitlines():
        first = None
        last = None
        for idx in range(len(line)):
            num = None
            if line[idx].isdigit():
                num = line[idx]
            for (key, val) in to_digit.items():
                if line[idx:].startswith(key):
                    num = val
                    break

            if num is not None:
                if first is None:
                    first = num
                last = num
        nums.append(int(first + last))
    return sum(nums)


if __name__ == "__main__":
    file = "input.txt"
    with open(file) as f:
        data = f.read()
        print(part1(data))
        print(part2(data))
