use std::collections::HashMap;
use std::fs;

fn main() {
    let file_path = "inputs/day_.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let part1_sol = part1();

    println!("Part1: {}", part1_sol);

    let part2_sol = part2();

    println!("Part2: {}", part2_sol);
}

fn part1() -> i32 {
    0
}

fn part2() -> i32 {
    0
}
