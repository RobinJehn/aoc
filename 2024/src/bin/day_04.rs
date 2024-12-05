use std::fs;

fn main() {
    let file_path = "inputs/day_04.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let grid: Vec<Vec<char>> = contents
        .lines()
        .map(|line| line.chars().collect())
        .collect();

    let save_reports = part1(&grid);

    println!("Save reports: {}", save_reports);

    let similarity_score = part2(&grid);

    println!("Similarity score: {}", similarity_score);
}

fn search(pattern: &str, delta_x: i32, delta_y: i32, grid: &Vec<Vec<char>>) -> i32 {
    let mut number_found = 0;
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            let mut found = true;
            for (k, c) in pattern.chars().enumerate() {
                let x = i as i32 + k as i32 * delta_x;
                let y = j as i32 + k as i32 * delta_y;
                if x < 0
                    || x >= grid.len() as i32
                    || y < 0
                    || y >= grid[0].len() as i32
                    || grid[x as usize][y as usize] != c
                {
                    found = false;
                    break;
                }
            }
            if found {
                number_found += 1;
            }
        }
    }

    number_found
}

fn part1(grid: &Vec<Vec<char>>) -> i32 {
    let pattern = "XMAS";

    let forwards = search(&pattern, 1, 0, &grid);
    let backwards = search(&pattern, -1, 0, &grid);
    let up = search(&pattern, 0, 1, &grid);
    let down = search(&pattern, 0, -1, &grid);
    let diagonal_up_right = search(&pattern, 1, 1, &grid);
    let diagonal_up_left = search(&pattern, -1, 1, &grid);
    let diagonal_down_right = search(&pattern, 1, -1, &grid);
    let diagonal_down_left = search(&pattern, -1, -1, &grid);

    return forwards
        + backwards
        + up
        + down
        + diagonal_up_right
        + diagonal_up_left
        + diagonal_down_right
        + diagonal_down_left;
}

fn search_locations(
    pattern: &str,
    delta_x: i32,
    delta_y: i32,
    grid: &Vec<Vec<char>>,
) -> Vec<(i32, i32)> {
    let mut locations_found = vec![];
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            let mut found = true;
            for (k, c) in pattern.chars().enumerate() {
                let x = i as i32 + k as i32 * delta_x;
                let y = j as i32 + k as i32 * delta_y;
                if x < 0
                    || x >= grid.len() as i32
                    || y < 0
                    || y >= grid[0].len() as i32
                    || grid[x as usize][y as usize] != c
                {
                    found = false;
                    break;
                }
            }
            if found {
                let middle_x = i as i32 + (pattern.len() as i32 - 1) * delta_x / 2;
                let middle_y = j as i32 + (pattern.len() as i32 - 1) * delta_y / 2;
                locations_found.push((middle_x, middle_y));
            }
        }
    }

    locations_found
}

fn part2(grid: &Vec<Vec<char>>) -> i32 {
    let pattern = "MAS";

    let diagonal_up_right = search_locations(&pattern, 1, 1, &grid);
    let diagonal_up_left = search_locations(&pattern, -1, 1, &grid);
    let diagonal_down_right = search_locations(&pattern, 1, -1, &grid);
    let diagonal_down_left = search_locations(&pattern, -1, -1, &grid);

    let all_locations = [
        diagonal_up_right,
        diagonal_up_left,
        diagonal_down_right,
        diagonal_down_left,
    ]
    .concat();

    let mut counts = std::collections::HashMap::new();
    for location in &all_locations {
        if let Some(count) = counts.get(location) {
            counts.insert(location, count + 1);
        } else {
            counts.insert(location, 1);
        }
    }

    let mut masses = 0;
    for count in counts.values() {
        if *count == 2 {
            masses += 1;
        }
    }

    masses
}
