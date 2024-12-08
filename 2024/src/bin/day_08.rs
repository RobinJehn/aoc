use std::collections::{HashMap, HashSet};
use std::fs;
use std::hash::{Hash, Hasher};

#[derive(Clone, Copy)]
struct Pos {
    x: i32,
    y: i32,
}

impl Pos {
    fn in_grid(&self, grid: &Vec<Vec<char>>) -> bool {
        self.x >= 0 && self.x < grid.len() as i32 && self.y >= 0 && self.y < grid[0].len() as i32
    }
}

impl Hash for Pos {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.x.hash(state);
        self.y.hash(state);
    }
}

impl Eq for Pos {}

impl PartialEq for Pos {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y
    }
}

impl std::ops::Sub for &Pos {
    type Output = Pos;

    fn sub(self, other: Self) -> Self::Output {
        Pos {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

impl std::ops::Sub for Pos {
    type Output = Pos;

    fn sub(self, other: Self) -> Self::Output {
        Pos {
            x: self.x - other.x,
            y: self.y - other.y,
        }
    }
}

impl std::ops::Add for Pos {
    type Output = Pos;

    fn add(self, other: Self) -> Self::Output {
        Pos {
            x: self.x + other.x,
            y: self.y + other.y,
        }
    }
}

fn main() {
    let file_path = "inputs/day_08.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let mut grid: Vec<Vec<char>> = vec![];
    for line in contents.lines() {
        let row: Vec<char> = line.chars().collect();
        grid.push(row);
    }

    let mut antennas: HashMap<char, Vec<Pos>> = HashMap::new();
    for i in 0..grid.len() {
        for j in 0..grid[i].len() {
            let c = grid[i][j];
            if c != '.' {
                let ant = Pos {
                    x: i as i32,
                    y: j as i32,
                };
                let entry = antennas.entry(c).or_insert(vec![]);
                entry.push(ant);
            }
        }
    }

    let part1_sol = part1(&grid, &antennas);

    println!("Part1: {}", part1_sol);

    let part2_sol = part2(&grid, &antennas);

    println!("Part2: {}", part2_sol);
}

fn part1(grid: &Vec<Vec<char>>, antennas: &HashMap<char, Vec<Pos>>) -> i32 {
    let mut antinodes: HashSet<Pos> = HashSet::new();

    for (_, ants) in antennas.iter() {
        for i in 0..ants.len() {
            for j in (i + 1)..ants.len() {
                let ant_a = ants[i];
                let ant_b = ants[j];

                let pos_diff = ant_a - ant_b;

                let antinode_a = ant_a + pos_diff;
                let antinode_b = ant_b - pos_diff;

                if antinode_a.in_grid(grid) {
                    antinodes.insert(antinode_a);
                }
                if antinode_b.in_grid(grid) {
                    antinodes.insert(antinode_b);
                }
            }
        }
    }

    antinodes.len().try_into().unwrap()
}

fn part2(grid: &Vec<Vec<char>>, antennas: &HashMap<char, Vec<Pos>>) -> i32 {
    let mut antinodes: HashSet<Pos> = HashSet::new();

    for (_, ants) in antennas.iter() {
        for i in 0..ants.len() {
            for j in (i + 1)..ants.len() {
                let ant_a = ants[i];
                let ant_b = ants[j];
                let pos_diff = ant_a - ant_b;

                let mut antinode = ant_a;
                loop {
                    if !antinode.in_grid(grid) {
                        break;
                    }

                    antinodes.insert(antinode.clone());

                    antinode = antinode + pos_diff;
                }

                antinode = ant_a;
                loop {
                    if !antinode.in_grid(grid) {
                        break;
                    }

                    antinodes.insert(antinode.clone());

                    antinode = antinode - pos_diff;
                }
            }
        }
    }

    antinodes.len().try_into().unwrap()
}
