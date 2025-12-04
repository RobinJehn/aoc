use std::collections::HashMap;
use std::fs;

fn main() {
    let file_path = "inputs/day_04.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    //     let contents = "..@@.@@@@.
    // @@@.@.@.@@
    // @@@@@.@.@@
    // @.@@@@..@.
    // @@.@@@@.@@
    // .@@@@@@@.@
    // .@.@.@.@@@
    // @.@@@.@@@@
    // .@@@@@@@@.
    // @.@.@@@.@.";

    let mut grid: Vec<Vec<char>> = Vec::new();
    for line in contents.lines() {
        grid.push(line.trim().chars().collect());
    }

    let part1_sol = part1(&grid);

    println!("Part1: {}", part1_sol);

    let part2_sol = part2(&grid);

    println!("Part2: {}", part2_sol);
}

fn part1(grid: &Vec<Vec<char>>) -> i32 {
    let rows = grid.len();
    let columns = grid[0].len();

    let mut rolls = 0;
    for r in 0..rows {
        for c in 0..columns {
            if grid[r][c] != '@' {
                continue;
            }
            let mut count = 0;
            for i in -1i32..=1 {
                let row = r as i32 + i;
                if row < 0 || row >= rows as i32 {
                    continue;
                }
                for j in -1i32..=1 {
                    if i == 0 && j == 0 {
                        continue;
                    }
                    let column = c as i32 + j;
                    if column < 0 || column >= columns as i32 {
                        continue;
                    }
                    if grid[row as usize][column as usize] == '@' {
                        count += 1;
                    }
                }
            }
            if count < 4 {
                rolls += 1;
            }
        }
    }
    return rolls;
}

fn remove(grid: &mut Vec<Vec<char>>) -> i32 {
    let rows = grid.len();
    let columns = grid[0].len();

    let mut rolls = 0;
    for r in 0..rows {
        for c in 0..columns {
            if grid[r][c] != '@' {
                continue;
            }
            let mut count = 0;
            for i in -1i32..=1 {
                let row = r as i32 + i;
                if row < 0 || row >= rows as i32 {
                    continue;
                }
                for j in -1i32..=1 {
                    if i == 0 && j == 0 {
                        continue;
                    }
                    let column = c as i32 + j;
                    if column < 0 || column >= columns as i32 {
                        continue;
                    }
                    if grid[row as usize][column as usize] == '@' {
                        count += 1;
                    }
                }
            }
            if count < 4 {
                grid[r][c] = '.';
                rolls += 1;
            }
        }
    }
    return rolls;
}

fn part2(grid: &Vec<Vec<char>>) -> i32 {
    let mut grid_copy = grid.clone();
    let mut tot_rolls_removed = 0;
    while true {
        let rolls_removed = remove(&mut grid_copy);
        if rolls_removed == 0 {
            break;
        }
        tot_rolls_removed += rolls_removed;
    }

    return tot_rolls_removed;
}
