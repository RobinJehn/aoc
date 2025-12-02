use std::collections::HashMap;
use std::{fs, usize};

fn main() {
    let file_path = "inputs/day_02.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    // let contents = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124";
    let mut ranges: Vec<(i64, i64)> = Vec::new();
    for range in contents.split(",") {
        let mut parts = range.trim_end().split("-");
        let from: i64 = parts.next().unwrap().parse().unwrap();
        let to: i64 = parts.next().unwrap().parse().unwrap();
        ranges.push((from, to));
    }

    let part1_sol = part1(&ranges);

    println!("Part1: {}", part1_sol);

    let part2_sol = part2(&ranges);

    println!("Part2: {}", part2_sol);
}

fn part1(ranges: &Vec<(i64, i64)>) -> i64 {
    let mut res = 0;
    for range in ranges {
        for val in range.0..range.1 {
            let val_str = val.to_string();
            if val_str.len().rem_euclid(2) != 0 {
                continue;
            }
            let len = val_str.len();
            if val_str[..len / 2] == val_str[len / 2..] {
                // println!("{}", val_str);
                res += val;
            }
        }
    }
    res
}

fn divisors(n: usize) -> Vec<usize> {
    let mut divs = Vec::new();

    let mut i = 1;
    while i < n {
        if n % i == 0 {
            divs.push(i);
        }
        i += 1;
    }
    return divs;
}

fn part2(ranges: &Vec<(i64, i64)>) -> i64 {
    let mut res = 0;
    for range in ranges {
        for val in range.0..=range.1 {
            let val_str = val.to_string();
            let len = val_str.len();
            let divs = divisors(len);
            for div in divs {
                let part = &val_str[..div];
                let mut is_same = true;
                for i in 1..(len / div) {
                    is_same &= part == &val_str[i * div..(i + 1) * div];
                }
                if is_same {
                    res += val;
                    break;
                }
            }
        }
    }
    res
}
