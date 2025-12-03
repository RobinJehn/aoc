use std::collections::HashMap;
use std::fs;

fn main() {
    let file_path = "inputs/day_03.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");
    //     let contents = "987654321111111
    // 811111111111119
    // 234234234234278
    // 818181911112111
    // ";
    let part1_sol = part1(&contents);

    println!("Part1: {}", part1_sol);

    let part2_sol = part2(&contents);

    println!("Part2: {}", part2_sol);
}

fn find_largest_num(cs: &Vec<char>, start_pos: usize, length: usize) -> u64 {
    if length == 0 {
        return 0;
    }
    let mut highest_found: u64 = 0;
    let mut highest_found_pos = 0;
    for i in start_pos..cs.len() - length + 1 {
        let c = cs[i];
        let val: u64 = c.to_digit(10).unwrap() as u64;
        if val > highest_found {
            highest_found = val;
            highest_found_pos = i;
        }
    }
    let t = (10 as u64).pow((length - 1) as u32) * highest_found;
    return t + find_largest_num(cs, highest_found_pos + (1 as usize), length - 1);
}

fn part1(contents: &str) -> u64 {
    let mut res = 0;
    for line in contents.lines() {
        let cs: Vec<char> = line.trim_end().chars().collect();
        let val = find_largest_num(&cs, 0, 2);
        res += val;
    }
    return res;
}

fn part2(contents: &str) -> u64 {
    let mut res = 0;
    for line in contents.lines() {
        let cs: Vec<char> = line.trim_end().chars().collect();
        let val = find_largest_num(&cs, 0, 12);
        res += val;
    }
    return res;
}
