use std::{fs, vec};

struct Equation {
    lhs: i64,
    rhs: Vec<i64>,
}

fn main() {
    let file_path = "inputs/day_07.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let mut equations = vec![];
    for line in contents.lines() {
        let mut parts = line.split(": ");
        let lhs = parts.next().unwrap();
        let rhs = parts.next().unwrap();

        let rhs_parts = rhs
            .split(" ")
            .map(|x| x.parse::<i64>().unwrap())
            .collect::<Vec<i64>>();

        equations.push(Equation {
            lhs: lhs.parse::<i64>().unwrap(),
            rhs: rhs_parts,
        });
    }

    let part1_sol = part1(&equations);

    println!("Part1: {}", part1_sol);

    let part2_sol = part2(&equations);

    println!("Part2: {}", part2_sol);
}

fn is_valid(equation: &Equation) -> bool {
    let operators = vec!["+", "*"];
    let num_operators_req = equation.rhs.len();

    for i in 0..(operators.len().pow(num_operators_req as u32)) {
        let mut result = 0;
        for j in 0..num_operators_req {
            let operator = operators[(i / operators.len().pow(j as u32)) % operators.len()];
            match operator {
                "+" => result += equation.rhs[j],
                "*" => result *= equation.rhs[j],
                _ => panic!("Unknown operator"),
            }
        }
        if result == equation.lhs {
            return true;
        }
    }

    false
}

fn part1(equations: &Vec<Equation>) -> i64 {
    let mut result = 0;
    for eq in equations {
        if is_valid(eq) {
            result += eq.lhs;
        }
    }
    result
}

fn is_valid_extended(equation: &Equation) -> bool {
    let operators = vec!["+", "*", "||"];
    let num_operators_req = equation.rhs.len() - 1;

    for i in 0..(operators.len().pow(num_operators_req as u32)) {
        let mut result = equation.rhs[0];

        for j in 0..num_operators_req {
            let operator = operators[(i / operators.len().pow(j as u32)) % operators.len()];

            match operator {
                "+" => result += equation.rhs[j + 1],
                "*" => result *= equation.rhs[j + 1],
                "||" => {
                    result = result * (10 as i64).pow(equation.rhs[j + 1].to_string().len() as u32)
                        + equation.rhs[j + 1];
                }
                _ => panic!("Unknown operator"),
            }
        }
        if result == equation.lhs {
            return true;
        }
    }

    false
}

fn part2(equations: &Vec<Equation>) -> i64 {
    let mut result = 0;
    for eq in equations {
        if is_valid_extended(eq) {
            result += eq.lhs;
        }
    }
    result
}
