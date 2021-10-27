from typing import *
from config import *
from http_service_utils import *

import gc
import os
from collections import Counter
from time import perf_counter

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
