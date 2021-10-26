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
Results per second are temporarily stored in files and merged in 10 minutes intervals.

## Where to access the data?
The crawler will be hosted on Lightsail with API access to the data soon.

## Remark
- The searching rate on Lexi-can is around 100 characters per minute.
- Character repeatedly searched, before leaving the 50-char list, appears once only but with time updated.

## TO-DO
- [ ] Host the crawler on Lightsail.
- [ ] Web API for data access (with FastAPI).
- [ ] Start-up script for launching the crawler and web service.
- [ ] Analyse log and finetune crawling interval.