import os
from typing import *
from datetime import datetime, timedelta, timezone
from time import sleep
import logging
from logging.handlers import RotatingFileHandler
import requests
from bs4 import BeautifulSoup, Tag

# Config
URL_JUST = "https://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/just.php"
SIZE_LOG = 1024 * 1024 * 10
TZ_HK = timezone(timedelta(hours=8))
POLL_INTERVAL = 10 # In Seconds
MERGE_INTERVAL = 10 # In minutes
MERGE_INTERVAL_SEC = MERGE_INTERVAL * 60

# Files
FILE_LOG = "log/crawl.log"
DIR_DB  = "lexican.db"
DIR_DB_MERGED  = "lexican.merged.db"

def crawl_new_words():
    # Obtain the webpage and prase the page
    resp = requests.get(URL_JUST, verify=False)
    assert resp.status_code == 200, "Cannot retrieve table."
    resp.encoding = resp.apparent_encoding
    html_code = resp.text
    prased = BeautifulSoup(html_code, "lxml")

    # Turn the prased page into a dictionary
    crawled_records = {}
    for i, row in enumerate(prased.find_all('tr')):  # type: int, Tag
        if i == 0: continue
        ch, time = (c.text for c in row.contents)
        timestamp = str(int(datetime.strptime(time, '%Y-%m-%d %H:%M:%S').replace(tzinfo=TZ_HK).timestamp()))
        crawled_records[timestamp] = crawled_records.get(timestamp, []) + [ch]

    # Load existing data as dictionary
    old_recs = {
        ts: [] if not os.path.exists(
            (old_file := os.path.join(DIR_DB, ts))
        ) else [ch for ch in open(old_file, "r").readline()]
        for ts in crawled_records.keys()
    }

    # Filter out files without new charater
    cnt_new_chs = 0
    for ts, chs in crawled_records.items():
        if all(ch in old_recs[ts] for ch in chs):
            crawled_records[ts] = None
        else:
            # Merge Results
            crawled_records[ts] = list(set(crawled_records[ts] + old_recs[ts]))
            cnt_new_chs += len(crawled_records[ts]) - len(old_recs[ts])

    # Update records
    for ts, chs in crawled_records.items():
        if chs is not None:
            with open(os.path.join(DIR_DB, ts), "w") as f:
                f.write(''.join(chs))

    logging.info(f"Crawl new words: {cnt_new_chs}")

def merge_files():
    # Calculate latest file to be merged
    now = datetime.now().replace(second=0, microsecond=0)
    td = timedelta(minutes=(MERGE_INTERVAL + now.minute % MERGE_INTERVAL))
    max_time = now - td
    max_ts = int(max_time.timestamp())

    # Obtain file names (Timestamps)
    file_list = [
        f_int for f in os.listdir(DIR_DB)
        if f[0] != '.' and (f_int := int(f)) < max_ts
    ]
    if not file_list: return
    file_list.sort()
    min_ts = file_list[0]
    min_ts -= min_ts % (MERGE_INTERVAL_SEC)

    # Divide files according to interval
    merge_list = {
        ts_start: []
        for ts_start in range(min_ts, max_ts, MERGE_INTERVAL_SEC)
    }
    for f_int in file_list:
        merge_list[f_int - (f_int % MERGE_INTERVAL_SEC)].append(os.path.join(DIR_DB, str(f_int)))

    for output_ts, input_files in merge_list.items():
        with open(os.path.join(DIR_DB_MERGED, str(output_ts)), 'w') as f_out:
            f_out.write(''.join([open(f_in).readline() for f_in in input_files]))
        for f_in in input_files:
            os.unlink(f_in)

    file_merged = len(file_list)
    logging.info(f"Merged files: {file_merged}")

if __name__ == "__main__":
    # Setup Log
    logging.basicConfig(level=logging.INFO,
        format = '%(asctime)s %(levelname)s %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        handlers = [RotatingFileHandler(FILE_LOG, mode='a', maxBytes=SIZE_LOG, backupCount=10, encoding='utf-8'), ]
    )
    while True:
        try:
            crawl_new_words()
            merge_files()
            sleep(POLL_INTERVAL)
        except Exception as e:
            logging.error(e)





