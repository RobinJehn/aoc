def part1():
    engine_schematic = []
    special_characters = []
    with open('input.txt') as f:
        data = f.read().splitlines()
        for l_idx, line in enumerate(data):
            line_list = []
            for c_idx, char in enumerate(line):
                line_list.append(char)
                if char == '.' or char.isdigit():
                    continue
                special_characters.append((l_idx, c_idx))

            engine_schematic.append(line_list)

    n_lines = len(engine_schematic)
    n_columns = len(engine_schematic[0])

    found_numbers = []
    for l_idx, c_idx in special_characters:
        for i in range (-1,2,1):
            for j in range (-1,2,1):
                if l_idx+i < 0 or l_idx+i >= n_lines or c_idx+j < 0 or c_idx+j >= n_columns:
                    continue

                if engine_schematic[l_idx+i][c_idx+j].isdigit():
                    start_c_idx = c_idx+j
                    end_c_idx = c_idx+j
                    while start_c_idx-1 >= 0 and engine_schematic[l_idx+i][start_c_idx-1].isdigit():
                        start_c_idx -= 1
                    while end_c_idx+1 < n_columns and engine_schematic[l_idx+i][end_c_idx+1].isdigit():
                        end_c_idx += 1

                    if (start_c_idx, end_c_idx, l_idx+i) not in found_numbers:
                        found_numbers.append((start_c_idx, end_c_idx, l_idx+i))

    total = 0   
    for found_number in found_numbers:
        start_c_idx, end_c_idx, l_idx = found_number
        string_num = "".join(engine_schematic[l_idx][start_c_idx:end_c_idx+1])
        total += int(string_num)
    return total

def part2():
    engine_schematic = []
    special_characters = []
    with open('input.txt') as f:
        data = f.read().splitlines()
        for l_idx, line in enumerate(data):
            line_list = []
            for c_idx, char in enumerate(line):
                line_list.append(char)
                if char == '*':
                    special_characters.append((l_idx, c_idx))

            engine_schematic.append(line_list)

    n_lines = len(engine_schematic)
    n_columns = len(engine_schematic[0])

    found_numbers = []
    for l_idx, c_idx in special_characters:
        found_numbers_guess = []
        for i in range (-1,2,1):
            for j in range (-1,2,1):
                if l_idx+i < 0 or l_idx+i >= n_lines or c_idx+j < 0 or c_idx+j >= n_columns:
                    continue

                if engine_schematic[l_idx+i][c_idx+j].isdigit():
                    start_c_idx = c_idx+j
                    end_c_idx = c_idx+j
                    while start_c_idx-1 >= 0 and engine_schematic[l_idx+i][start_c_idx-1].isdigit():
                        start_c_idx -= 1
                    while end_c_idx+1 < n_columns and engine_schematic[l_idx+i][end_c_idx+1].isdigit():
                        end_c_idx += 1

                    if (start_c_idx, end_c_idx, l_idx+i) not in found_numbers_guess:
                        found_numbers_guess.append((start_c_idx, end_c_idx, l_idx+i))
        if len(found_numbers_guess) == 2:
            found_numbers.append(found_numbers_guess)

    total = 0   
    for found_number_parts in found_numbers:
        found_number1, found_number2 = found_number_parts
        start_c_idx1, end_c_idx1, l_idx1 = found_number1
        string_num1 = "".join(engine_schematic[l_idx1][start_c_idx1:end_c_idx1+1])
        start_c_idx2, end_c_idx2, l_idx2 = found_number2
        string_num2 = "".join(engine_schematic[l_idx2][start_c_idx2:end_c_idx2+1])
        total += int(string_num1) * int(string_num2)
    return total

if __name__ == "__main__":
    print(part1())
    print(part2())