def part1(data):
    allowed_cubes = {"red": 12, "green": 13, "blue": 14}
    allowed_games = []
    for line in data.splitlines():
        id_str, game_str = line.split(":")
        id = int(id_str[5:])
        valid = True
        for draw in game_str.split(";"):
            cubes = draw.split(",")
            for cube in cubes:
                splitted = cube.split(" ")
                if len(splitted) != 2:
                    num, color = splitted[1:]
                else:
                    num, color = splitted
                if int(num) > allowed_cubes[color]:
                    valid = False
        if valid:
            allowed_games.append(id)
    return sum(allowed_games)


def part2(data):
    allowed_games = []
    for line in data.splitlines():
        _, game_str = line.split(":")
        allowed_cubes = {"red": 0, "green": 0, "blue": 0}
        for draw in game_str.split(";"):
            cubes = draw.split(",")
            for cube in cubes:
                splitted = cube.split(" ")
                if len(splitted) != 2:
                    num, color = splitted[1:]
                else:
                    num, color = splitted
                allowed_cubes[color] = max(allowed_cubes[color], int(num))
        value = 1
        for _, val in allowed_cubes.items():
            if val == 0:
                continue
            value *= val
        allowed_games.append(value)
    return sum(allowed_games)


if __name__ == "__main__":
    file = "input.txt"
    with open(file) as f:
        data = f.read()
        print(part1(data))
        print(part2(data))
