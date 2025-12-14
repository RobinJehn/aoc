use std::collections::HashMap;
use std::{fs, num};

fn main() {
    let file_path = "inputs/day_06.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");
    //     let contents = "123 328  51 64
    //  45 64  387 23
    //   6 98  215 314
    // *   +   *   +  ";
    //
    let mut expr: Vec<Vec<&str>> = Vec::new();
    let mut first_line = true;
    for line in contents.lines() {
        let columns = line.split_whitespace();
        for (idx, col) in columns.enumerate() {
            if first_line {
                let new_vec: Vec<&str> = Vec::new();
                expr.push(new_vec);
            }

            expr[idx].push(col);
        }
        first_line = false;
    }

    let part1_sol = part1(&expr);

    println!("Part1: {}", part1_sol);

    let part2_sol = part2(&contents);

    println!("Part2: {}", part2_sol);
}

fn part1(expr: &Vec<Vec<&str>>) -> i64 {
    let mut total_res = 0;
    for exp in expr {
        let operator = exp[exp.len() - 1];
        let mut result: i64 = exp[0].parse().unwrap();
        for i in 1..exp.len() - 1 {
            let value: i64 = exp[i].parse().unwrap();
            if operator == "+" {
                result += value;
            } else if operator == "*" {
                result *= value;
            }
        }
        total_res += result
    }
    return total_res;
}

fn part2(contents: &str) -> i64 {
    let num_lines = contents.lines().count();
    let mut columns: Vec<String> = Vec::new();
    let mut operators: Vec<&str> = Vec::new();
    for (idx, line) in contents.lines().enumerate() {
        if idx == num_lines - 1 {
            operators = line.split_whitespace().collect();
        } else {
            for (idx, char) in line.chars().enumerate() {
                if idx + 1 > columns.len() {
                    columns.push(String::new());
                }
                columns[idx].push(char);
            }
        }
    }

    let mut operation = 0;
    let mut total_result = 0;
    let mut current_result = 0;
    for column in columns {
        if column.trim().is_empty() {
            operation += 1;
            total_result += current_result;
            current_result = 0;
            continue;
        }

        let value: i64 = column.trim().parse().unwrap();
        if current_result == 0 {
            current_result = value
        } else {
            if operators[operation] == "*" {
                current_result *= value;
            } else {
                current_result += value;
            }
        }
    }
    total_result += current_result;

    return total_result;
}
