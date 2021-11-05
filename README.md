# Lexi-Can Search History Crawler 
Crawler which captures the usage history of CUHK Lexi-Can (粵語審音配詞字庫).
https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/

## Objective
Finding out Cantonese speakers are curious about which Chinese characters.

## Background
["The Chinese Character Database: With Word-formations Phonologically Disambiguated According to the Cantonese Dialect"](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/) is one of the most commonly used Cantonese lexicons, led by Prof. Tze-wan Kwan (關子尹) and published since 2003.

The lexicon lists [50 recently searched characters](https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/just.php) (in PHP), from both search box and direct links on the site.
However, historical results are not available to the public.

## What does the crawler do?
It polls and parses the search record every 10 seconds.
Results per second are temporarily stored in files and merged in 30 minutes intervals.

## Where to access the data?
The crawler will be hosted on Lightsail with API access to the data soon.

## Requirement
Python 3.9 + Sqlite
Lightsail + Stock Amazon Linux 2 cannot meet the requirements with "yum" alone.

Quick cookbook:
``` Bash
# Install Sqlite
sudo yum install sqlite-devel

# Compile and install Python 3.9
wget https://www.python.org/ftp/python/3.9.6/Python-3.9.6.tgz
# Untar the source and cd.
./configure --enable-optimizations
sudo make altinstall
```
Remaining are `pip install -r requirements.txt` and `crontab -e` according crontab_config.

## Remark
- The searching rate on Lexi-can is around 100 characters per minute.
- Character repeatedly searched, before leaving the 50-char list, appears once only but with time updated.
- One of the greatest concerns is that the crawler hosts on Lightsail with the lowest capability (1 CPU, 0.5GB RAM). Examples are how we modify lru_cache into "cache_on_latest_ts" and revision on "get_latest_file".

## TO-DO
- [x] Host the crawler on Lightsail.
- [x] Web API for data access (with FastAPI).
- [x] Select stats from an interval.
- [ ] Think of functions provided by the service. (Generated Graphics?)
- [x] Start-up script for launching the crawler and web service.
- [ ] Analyse log and finetune crawling interval.
