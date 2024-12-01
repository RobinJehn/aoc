use std::collections::HashMap;
use std::{fs, vec};

fn main() {
    let file_path = "inputs/day_01.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let mut vec_1 = vec![];
    let mut vec_2 = vec![];
    for line in contents.lines() {
        let mut iter = line.split_whitespace();
        let first = iter.next().unwrap();
        let second = iter.next().unwrap();

        let first_num: i32 = first.parse().expect("Failed to parse");
        let second_num: i32 = second.parse().expect("Failed to parse");

        vec_1.push(first_num);
        vec_2.push(second_num);
    }

    vec_1.sort();
    vec_2.sort();

    let total_diff = part1(&vec_1, &vec_2);

    println!("Total diff: {}", total_diff);

    let similarity_score = part2(&vec_1, &vec_2);

    println!("Similarity score: {}", similarity_score);
}

fn part1(vec_1: &Vec<i32>, vec_2: &Vec<i32>) -> i32 {
    let mut total_diff = 0;
    for (a, b) in vec_1.iter().zip(vec_2.iter()) {
        total_diff += (a - b).abs();
    }

    total_diff
}

fn part2(vec_1: &Vec<i32>, vec_2: &Vec<i32>) -> i32 {
    let mut number_of_appearences = HashMap::new();

    for num in vec_2.iter() {
        if let Some(count) = number_of_appearences.get(num) {
            number_of_appearences.insert(num, count + 1);
        } else {
            number_of_appearences.insert(num, 1);
        }
    }

    let mut similarity_score = 0;

    for num in vec_1.iter() {
        if let Some(count) = number_of_appearences.get(num) {
            similarity_score += count * num;
        }
    }

    similarity_score
}
