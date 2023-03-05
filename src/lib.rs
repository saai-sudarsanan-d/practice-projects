use std::{fs, error::Error,time::Instant};
use colored::*;

pub struct Config {
    pub query: String,
    pub flags: String,
    pub filename: String,
}

impl Config {
    pub fn new(args: &[String]) -> Result<Config, &str> {

        if args.len() < 3 {
            return Err("Not enough arguements!");
        }

        let mut flags = "".to_string();
        let filename;

        let query = args[1].clone();
        if args[2].starts_with('-') {
            flags = args[2].clone();
            filename = args[3].clone();
        } else {
            filename = args[2].clone();
        }
        Ok(Config {query,flags,filename})
    }    
}

pub struct SearchResults<'a>{
    results : Vec<(usize, &'a str)>,
    count : u64
}

pub fn search<'a>(query: &str, contents: &'a str,flags:&str) -> SearchResults<'a>{
    let mut results = Vec::new();
    let query = query;
    let mut count:u64 = 0;

    if flags.contains('v') {
        for line in contents.lines().enumerate(){
            if !line.1.contains(&query){
                count += line.1.matches(&query).count() as u64;
                results.push((line.0,line.1));
            }
        }
    } 
    else{
        for line in contents.lines().enumerate(){
            if line.1.contains(&query){
                count += line.1.matches(&query).count() as u64;
                results.push((line.0,line.1));
            }
        }
    }
    SearchResults { results,count }
}

pub fn documentation(){
    println!("{} ./minigrep <query> <flags> <filename>","USAGE :".blue().bold());
    println!("{} Print the Number of Occurences of the Query","-c".red().bold());
    println!("{} Invert Selection","-v".red().bold());
    println!("{} Print line numbers","-l".red().bold());
    println!("{} Print the time elapsed in searching","-t".red().bold());
}

pub fn run(config:Config) -> Result<(),Box<dyn Error>> {
    println!("Searching for {}",config.query);
    println!("In File {}",config.filename);

    let contents = fs::read_to_string(config.filename)?;

    let start = Instant::now();
    let results = search(&config.query,&contents,&config.flags);
    let duration = start.elapsed();

    if config.flags.contains('l'){
        for line in results.results{
            println!("{} {}",line.0.to_string().green().bold(),line.1);
        }
    } else {
        for line in results.results{
            println!("{}",line.1);
        }
    }
    println!("{}","====================================".black());

    if config.flags.contains('c') {
        println!("{} {}","Number of Occurences :".red().bold(),results.count);
    }
    if config.flags.contains('t') {
        println!("{} {:?}","Time elapsed in searching is:".red().bold(), duration);
    }
    Ok(())
}