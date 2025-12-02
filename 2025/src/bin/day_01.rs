use std::fs;

fn part1(contents: &str) -> i32 {
    let mut dial_pos = 50;
    let mut count = 0;
    for line in contents.lines() {
        let dir: i32 = if line.chars().nth(0).unwrap() == 'L' {
            -1
        } else {
            1
        };
        let amount: i32 = line[1..].parse().expect("Failed to parse");

        dial_pos = (dir * amount + dial_pos).rem_euclid(100);
        if dial_pos == 0 {
            count += 1;
        }
    }
    return count;
}

fn part2(contents: &str) -> i32 {
    let mut dial_pos = 50;
    let mut count = 0;
    for line in contents.lines() {
        let dir: i32 = if line.chars().nth(0).unwrap() == 'L' {
            -1
        } else {
            1
        };
        let amount: i32 = line[1..].parse().expect("Failed to parse");

        let dial_pos_prev = dial_pos;
        dial_pos = dir * amount + dial_pos;

        if dial_pos.signum() != dial_pos_prev.signum() && dial_pos_prev != 0 {
            count += 1;
        }
        count += (dial_pos / 100).abs();
        dial_pos = dial_pos.rem_euclid(100);
    }
    return count;
}

fn main() {
    let file_path = "inputs/day_01.txt";
    let contents = fs::read_to_string(file_path).expect("Couldnt read the file");

    let part1_sol = part1(&contents);
    let part2_sol = part2(&contents);
    println!("{}", part1_sol);
    println!("{}", part2_sol);
}
