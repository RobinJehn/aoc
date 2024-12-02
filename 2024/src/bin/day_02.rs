use std::fs;

fn main() {
    let file_path = "inputs/day_02.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let save_reports = part1(&contents);

    println!("Save reports: {}", save_reports);

    let similarity_score = part2(&contents);

    println!("Similarity score: {}", similarity_score);
}

fn part1(contents: &String) -> i32 {
    let mut safe_reports = 0;
    for line in contents.lines() {
        let levels: Vec<i32> = line
            .split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect();
        if is_save(&levels) {
            safe_reports += 1;
        }
    }
    safe_reports
}

fn is_save(levels: &Vec<i32>) -> bool {
    let mut safe = true;
    let mut prev = levels[0];

    let direction = (levels[1] - prev).signum();
    for i in 1..levels.len() {
        let diff = levels[i] - prev;
        if diff.abs() > 3 || diff.abs() == 0 || direction != diff.signum() {
            safe = false;
            break;
        }

        prev = levels[i];
    }

    safe
}

fn get_permutations_missing_entry(levels: &Vec<i32>) -> Vec<Vec<i32>> {
    let mut permutations = Vec::new();
    for i in 0..levels.len() {
        let mut permutation = levels.clone();
        permutation.remove(i);
        permutations.push(permutation);
    }
    permutations
}

fn part2(contents: &String) -> i32 {
    let mut safe_reports = 0;
    for line in contents.lines() {
        let levels: Vec<i32> = line
            .split_whitespace()
            .map(|s| s.parse().unwrap())
            .collect();

        let permutations = get_permutations_missing_entry(&levels);
        for permutation in permutations {
            if is_save(&permutation) {
                safe_reports += 1;
                break;
            }
        }
    }
    safe_reports
}

// fn part2_old(contents: &String) -> i32 {
//     let mut safe_reports = 0;
//     for line in contents.lines() {
//         let mut iter = line.split_whitespace();
//         let mut direction = 0;

//         let mut removed = false;
//         let mut safe = true;
//         let mut prev = iter.next().unwrap().parse::<i32>().unwrap();
//         for i in iter {
//             let current = i.parse::<i32>().unwrap();
//             let diff = current - prev;
//             if diff.abs() > 3 || diff.abs() == 0 {
//                 if !removed {
//                     removed = true;
//                     continue;
//                 }

//                 safe = false;
//                 break;
//             }

//             if direction == 0 {
//                 direction = diff.signum();
//             } else if direction != diff.signum() {
//                 if !removed {
//                     removed = true;
//                     continue;
//                 }

//                 safe = false;
//                 break;
//             }

//             prev = current;
//         }

//         if safe {
//             safe_reports += 1;
//         }
//     }
//     safe_reports
// }
