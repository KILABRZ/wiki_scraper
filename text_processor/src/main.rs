use text_processor::*;
use std::io::Result as IoResult;
use std::fs::read_to_string;
use std::collections::HashMap;

const TARGET_DIR : &str = "../scraped_data";

fn main() -> IoResult<()> {

    let mut word_collector : HashMap<String, u64> = HashMap::new();

    for path in list_dir(TARGET_DIR)?.iter() {
        let mut s = read_to_string(&path).unwrap();
        s.make_ascii_lowercase();
        let s : String = s.chars().map(|c| {
            if c.is_ascii() && c.is_alphabetic() { c } else { ' ' }
        }).collect();
        let list_of_word : Vec<String> = s.split(' ').filter(|s| s.len() == 5).map(|s| s.to_string()).collect();
        for w in list_of_word.into_iter() {
            word_collector.entry(w).and_modify(|e| *e += 1).or_insert(1);
        }
    }

    let mut key_value : Vec<(String, u64)> = word_collector.into_iter().collect();

    key_value.sort_by_key(|a| -(a.1 as i64));

    for (i, (k, v)) in key_value.iter().enumerate() {
        print!("({}: {:4})     ", k, v);
        if i % 8 == 7 { println!(""); }
    }

    println!("");
    Ok(())
}
