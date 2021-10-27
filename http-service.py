from typing import *
from config import *
from http_service_utils import *

import gc
import os
from collections import Counter
from functools import lru_cache

from fastapi import FastAPI
# from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
# app.add_middleware(GZipMiddleware)

## Routines to read all data records
@cache_on_latest_file
def read_all_records() -> List[Dict[str,str]]:
    files = get_whole_file_list()
    return [
        {
            'time': ts,
            'words': open(os.path.join(DIR_DB_MERGED, ts)).readline()
        }
        for ts in files
    ]

@cache_on_latest_file
def count_all_data() -> List[Dict[str,str]]:
    recs = read_all_records()
    all_texts = ''.join(rec['words'] for rec in recs)
    return Counter(all_texts)

def read_log() -> List[str]:
    return [line.strip() for line in open(FILE_LOG_CRAWL,'r').readlines()]

@app.get("/")
def read_root():
    return {'just to':'say hi, again.'}

@app.get("/update_server")
def update_service():
    os.system("git pull")
    return {'result':'done'}

# API Call to get all data
@app.get("/all")
def get_all_records():
    return read_all_records()  

# API Call to count all data
@app.get("/all/count")
def get_all_count():
    result =  count_all_data()
    return result

# API Call of Logs
@app.get("/log/crawl")
def get_log_crawl():
    logs = [ line.split(' ') for line in read_log() if 'Crawl' in line ]
    return [
        {'time':' '.join((words[0],words[1])), 'words': int(words[-1])}
        for words in logs
    ]

@app.get("/log/merge")
def get_log_merge():
    logs = [line.split(' ') for line in read_log() if 'Merge' in line]
    return [
        {'time': ' '.join((words[0], words[1])), 'files': int(words[-1])}
        for words in logs
    ]

@app.get("/log/error")
def get_log_crawl():
    return [line for line in read_log() if 'ERROR' in line]
