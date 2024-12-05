use std::collections::HashMap;
use std::fs;

fn main() {
    let file_path = "inputs/day_05.txt";
    let contents = fs::read_to_string(file_path).expect("Should have been able to read the file");

    let mut is_pages = false;
    let mut updates: Vec<Vec<i32>> = Vec::new();
    let mut ordering: HashMap<i32, Vec<i32>> = HashMap::new();
    for line in contents.lines() {
        if line.is_empty() {
            is_pages = true;
            continue;
        }

        if is_pages {
            updates.push(line.split(",").map(|x| x.parse::<i32>().unwrap()).collect());
        } else {
            let parts: Vec<i32> = line.split("|").map(|x| x.parse::<i32>().unwrap()).collect();
            let [first, second]: [i32; 2] = parts.try_into().unwrap();
            if let Some(next_pages) = ordering.get_mut(&first) {
                next_pages.push(second);
            } else {
                ordering.insert(first, vec![second]);
            }
        }
    }

    let save_reports = part1(&updates, &ordering);

    println!("Save reports: {}", save_reports);

    let similarity_score = part2(&updates, &ordering);

    println!("Similarity score: {}", similarity_score);
}

fn is_valid(pages: &Vec<i32>, ordering: &HashMap<i32, Vec<i32>>) -> bool {
    let mut valid = true;

    for i in 0..pages.len() {
        let page = pages[i];

        // For each page that comes after check whether page should came after
        for j in i + 1..pages.len() {
            let next_page = pages[j];
            if let Some(next_pages) = ordering.get(&next_page) {
                if next_pages.contains(&page) {
                    valid = false;
                    break;
                }
            }
        }
    }

    valid
}

fn part1(updates: &Vec<Vec<i32>>, ordering: &HashMap<i32, Vec<i32>>) -> i32 {
    let mut middle_values = 0;
    for pages in updates {
        if is_valid(&pages, &ordering) {
            middle_values += pages[(pages.len() - 1) / 2];
        }
    }
    middle_values
}

fn reorder(pages: &Vec<i32>, ordering: &HashMap<i32, Vec<i32>>) -> Vec<i32> {
    let mut ordered_pages = Vec::new();

    for _ in 0..pages.len() {
        for j in 0..pages.len() {
            let page = pages[j];
            if ordered_pages.contains(&page) {
                continue;
            }

            // Check whether page should come after any of the remaining pages
            let mut should_insert = true;
            for k in 0..pages.len() {
                let next_page = pages[k];
                if next_page == page || ordered_pages.contains(&next_page) {
                    continue;
                }

                if let Some(next_pages) = ordering.get(&next_page) {
                    if next_pages.contains(&page) {
                        should_insert = false;
                        break;
                    }
                }
            }
            if should_insert {
                ordered_pages.push(page);
                break;
            }
        }
    }

    ordered_pages
}

fn part2(updates: &Vec<Vec<i32>>, ordering: &HashMap<i32, Vec<i32>>) -> i32 {
    let mut middle_values = 0;
    for pages in updates {
        if !is_valid(&pages, &ordering) {
            let ordered_pages = reorder(&pages, &ordering);
            middle_values += ordered_pages[(ordered_pages.len() - 1) / 2];
        }
    }
    middle_values
}
