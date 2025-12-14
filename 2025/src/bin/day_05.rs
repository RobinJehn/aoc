use std::collections::HashMap;
use std::fs;

fn main() {
    let file_path = "inputs/day_05.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");
    //     let contents = "3-5
    // 10-14
    // 16-20
    // 12-18
    //
    // 1
    // 5
    // 8
    // 11
    // 17
    // 32";

    let mut ranges: Vec<(i64, i64)> = Vec::new();
    let mut ingredients: Vec<i64> = Vec::new();
    let mut ranges_section = true;
    for line in contents.lines() {
        if line.trim().is_empty() {
            ranges_section = false;
            continue;
        }

        if ranges_section {
            let mut range = line.split("-");
            let from = range.next().unwrap().parse().unwrap();
            let to = range.next().unwrap().parse().unwrap();
            ranges.push((from, to));
        } else {
            ingredients.push(line.parse().unwrap());
        }
    }

    let part1_sol = part1(&ranges, &ingredients);

    println!("Part1: {}", part1_sol);

    let part2_sol = part2(&ranges);

    println!("Part2: {}", part2_sol);
}

fn part1(ranges: &Vec<(i64, i64)>, ingredients: &Vec<i64>) -> i32 {
    let mut fresh = 0;
    for ingredient in ingredients {
        for range in ranges {
            if ingredient >= &range.0 && ingredient <= &range.1 {
                fresh += 1;
                break;
            }
        }
    }
    return fresh;
}

fn merge_ranges(range1: &(i64, i64), range2: &(i64, i64)) -> (i64, i64) {
    let from = std::cmp::min(range1.0, range2.0);
    let to = std::cmp::max(range1.1, range2.1);

    return (from, to);
}

fn inside(range: &(i64, i64), val: i64) -> bool {
    return val >= range.0 && val <= range.1;
}

fn overlap(range1: &(i64, i64), range2: &(i64, i64)) -> bool {
    return inside(range1, range2.0)
        || inside(range1, range2.1)
        || inside(range2, range1.0)
        || inside(range2, range1.1);
}

fn part2(ranges: &Vec<(i64, i64)>) -> i64 {
    let mut merged_ranges = ranges.clone();
    while true {
        let mut changed = false;
        'outer: for i in 0..merged_ranges.len() {
            for j in (i + 1)..merged_ranges.len() {
                if overlap(&merged_ranges[i], &merged_ranges[j]) {
                    let r1 = merged_ranges[i].clone();
                    let r2 = merged_ranges[j].clone();
                    let mgd_rge = merge_ranges(&r1, &r2);

                    // println!("Overlap {}-{} and {}-{}", r1.0, r1.1, r2.0, r2.1);
                    merged_ranges.swap_remove(j);
                    merged_ranges.swap_remove(i);
                    merged_ranges.push(mgd_rge);
                    changed = true;
                    break 'outer;
                }
            }
        }
        if !changed {
            break;
        }
    }

    let mut count = 0;
    for range in merged_ranges {
        // println!("{}-{}", range.0, range.1);
        count += 1 + range.1 - range.0;
    }

    return count;
}
