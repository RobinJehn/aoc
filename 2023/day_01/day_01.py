def part1():
    nums = []
    with open("input.txt") as f:
        data = f.read().splitlines()
        for line in data:
            first = None
            last = None
            for char in line:
                if char.isdigit():
                    if first is None:
                        first = char
                    last = char
            nums.append(int(first + last))
    return sum(nums)


def part2():
    nums = []
    digit_strings = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
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
    with open("input.txt") as f:
        data = f.read().splitlines()
        for line in data:
            first = None
            last = None
            for idx in range(len(line)):
                num = None
                if line[idx].isdigit():
                    num = line[idx]
                for digit in digit_strings:
                    if line[idx:].startswith(digit):
                        num = to_digit[digit]
                        break

                if num is not None:
                    if first is None:
                        first = num
                    last = num
            nums.append(int(first + last))
    return sum(nums)


if __name__ == "__main__":
    print(part1())
    print(part2())
