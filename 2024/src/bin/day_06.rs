use std::fs;

fn main() {
    let file_path = "inputs/day_06.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let mut grid: Vec<Vec<char>> = Vec::new();

    for line in contents.lines() {
        let mut row: Vec<char> = Vec::new();
        for c in line.chars() {
            row.push(c);
        }
        grid.push(row);
    }

    let part1_sol = part1(grid.clone());

    println!("Part1: {}", part1_sol);

    let part2_sol = part2(&grid);

    println!("Part2: {}", part2_sol);
}

fn find_char(grid: &Vec<Vec<char>>, c: char) -> (usize, usize) {
    for (i, row) in grid.iter().enumerate() {
        for (j, &c2) in row.iter().enumerate() {
            if c2 == c {
                return (i, j);
            }
        }
    }

    (0, 0)
}

fn rotate(dir: &(i32, i32)) -> (i32, i32) {
    if *dir == (1, 0) {
        return (0, -1);
    } else if *dir == (0, 1) {
        return (1, 0);
    } else if *dir == (-1, 0) {
        return (0, 1);
    } else {
        return (-1, 0);
    };
}

fn rotate_in_place(dir: &mut (i32, i32)) {
    if *dir == (1, 0) {
        *dir = (0, -1);
    } else if *dir == (0, 1) {
        *dir = (1, 0);
    } else if *dir == (-1, 0) {
        *dir = (0, 1);
    } else {
        *dir = (-1, 0);
    };
}

fn part1(mut grid: Vec<Vec<char>>) -> i32 {
    let mut current_pos = find_char(&grid, '^');

    let mut visited_fields = 0;
    grid[current_pos.0][current_pos.1] = 'X';
    visited_fields += 1;
    let mut current_dir: (i32, i32) = (-1, 0);
    loop {
        if current_pos.0 as i32 + current_dir.0 < 0
            || current_pos.0 as i32 + current_dir.0 >= grid.len() as i32
            || current_pos.1 as i32 + current_dir.1 < 0
            || current_pos.1 as i32 + current_dir.1 >= grid[0].len() as i32
        {
            break;
        }

        let new_pos = (
            current_pos.0 + current_dir.0 as usize,
            current_pos.1 + current_dir.1 as usize,
        );
        if grid[new_pos.0 as usize][new_pos.1 as usize] == '#' {
            rotate_in_place(&mut current_dir);
            continue;
        }

        current_pos = new_pos;
        if grid[current_pos.0][current_pos.1] == '.' {
            grid[current_pos.0][current_pos.1] = 'X';
            visited_fields += 1;
        }
    }

    visited_fields
}

fn part2(grid: &Vec<Vec<char>>) -> i32 {
    let mut number_of_loops = 0;
    for i in 0..grid.len() {

        for j in 0..grid[0].len() {
            let mut grid_copy = grid.clone();
            grid_copy[i][j] = '#';
            if check_if_loop(grid_copy) {
                number_of_loops += 1;
            }
        }
    }

    number_of_loops
}

fn check_if_loop(grid: Vec<Vec<char>>) -> bool {
    let mut current_pos = find_char(&grid, '^');

    let mut visited_fields: Vec<Vec<Vec<(i32, i32)>>> = Vec::new();
    for _ in 0..grid.len() {
        let mut row: Vec<Vec<(i32, i32)>> = Vec::new();
        for _ in 0..grid[0].len() {
            row.push(Vec::new());
        }
        visited_fields.push(row);
    }

    let mut current_dir: (i32, i32) = (-1, 0);
    visited_fields[current_pos.0][current_pos.1].push(current_dir);
    loop {
        if current_pos.0 as i32 + current_dir.0 < 0
            || current_pos.0 as i32 + current_dir.0 >= grid.len() as i32
            || current_pos.1 as i32 + current_dir.1 < 0
            || current_pos.1 as i32 + current_dir.1 >= grid[0].len() as i32
        {
            break;
        }

        let new_pos = (
            current_pos.0 + current_dir.0 as usize,
            current_pos.1 + current_dir.1 as usize,
        );
        if grid[new_pos.0 as usize][new_pos.1 as usize] == '#' {
            rotate_in_place(&mut current_dir);
            continue;
        }

        current_pos = new_pos;
        if visited_fields[current_pos.0][current_pos.1].contains(&current_dir) {
            return true;
        }

        visited_fields[current_pos.0][current_pos.1].push(current_dir);
    }

    false
}

fn part2_nice_but_wrong(grid: &Vec<Vec<char>>) -> i32 {
    let mut current_pos = find_char(&grid, '^');

    let mut visited_fields: Vec<Vec<Vec<(i32, i32)>>> = Vec::new();
    for _ in 0..grid.len() {
        let mut row: Vec<Vec<(i32, i32)>> = Vec::new();
        for _ in 0..grid[0].len() {
            row.push(Vec::new());
        }
        visited_fields.push(row);
    }

    let mut current_dir: (i32, i32) = (-1, 0);
    visited_fields[current_pos.0][current_pos.1].push(current_dir);
    let mut loops = 0;
    loop {
        if current_pos.0 as i32 + current_dir.0 < 0
            || current_pos.0 as i32 + current_dir.0 >= grid.len() as i32
            || current_pos.1 as i32 + current_dir.1 < 0
            || current_pos.1 as i32 + current_dir.1 >= grid[0].len() as i32
        {
            break;
        }

        let new_pos = (
            current_pos.0 + current_dir.0 as usize,
            current_pos.1 + current_dir.1 as usize,
        );
        if grid[new_pos.0 as usize][new_pos.1 as usize] == '#' {
            rotate_in_place(&mut current_dir);
            continue;
        }

        current_pos = new_pos;
        println!("Current pos: {:?}", current_pos);
        println!("{:?}", visited_fields[current_pos.0][current_pos.1]);

        let new_dir = rotate(&current_dir);
        if visited_fields[current_pos.0][current_pos.1].contains(&new_dir) {
            println!("Found loop at: {:?}", current_pos);
            loops += 1;
        }

        visited_fields[current_pos.0][current_pos.1].push(current_dir);
    }

    loops
}
