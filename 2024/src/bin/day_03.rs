use regex::Regex;
use std::fs;

fn main() {
    let file_path = "inputs/day_03.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let save_reports = part1(&contents);

    println!("Save reports: {}", save_reports);

    let similarity_score = part2(&contents);

    println!("Similarity score: {}", similarity_score);
}

fn part1(contents: &String) -> i32 {
    let re = Regex::new(r"mul\(-?(\d*),-?(\d*)\)").unwrap();

    let mut sum: i32 = 0;
    for (_full, [first, second]) in re.captures_iter(contents).map(|m| m.extract()) {
        sum += first.parse::<i32>().unwrap() * second.parse::<i32>().unwrap();
    }
    sum
}

fn part2(contents: &String) -> i32 {
    let re = Regex::new(r"mul\(-?(\d*),-?(\d*)\)|do(n't)?").unwrap();
    let re_mul = Regex::new(r"mul\(-?(\d*),-?(\d*)\)").unwrap();

    let mut sum: i32 = 0;
    let mut should_do = true;
    for full in re.find_iter(contents).map(|m| m.as_str()) {
        if full == "do" {
            should_do = true;
        } else if full == "don't" {
            should_do = false;
        } else {
            let (_full, [first, second]) = re_mul.captures(full).map(|m| m.extract()).unwrap();
            if should_do {
                sum += first.parse::<i32>().unwrap() * second.parse::<i32>().unwrap();
            }
        }
    }
    sum
}
