use std::fs::read_dir;
use std::path::PathBuf;
use std::io::Result as IoResult;

pub fn list_dir(str_as_path: &str) -> IoResult<Vec<PathBuf>> {
	let paths = read_dir(str_as_path)?;
	Ok(paths.into_iter().map(|p| p.unwrap().path().clone()).collect())
} 