from typing import *
from config import *
from http_service_utils import *

from sql_queries import *
import sqlite3

import gc
import os
from collections import Counter
from datetime import datetime

from fastapi import FastAPI, HTTPException
# from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
# app.add_middleware(GZipMiddleware)

# Error Response 
ERR_INVALID_WORD_COUNT = HTTPException(status_code=422,detail={'reason':'Invalid word count','valid_input':POSSIBLE_MOST_COUNT})
ERR_INVALID_MONTH = HTTPException(status_code=422,detail={'reason':'Invalid month','valid_input':[i for i in range(1,13)]})

def counting_from_str(input: str, count: int) -> List[List[Union[str, int]]]:
    counted = Counter(input)
    if count != 0: 
        counted = counted.most_common(count)
    else:
        counted = sorted(counted.items(),key=lambda pair: pair[1],reverse=True)
    counted = [('ch','cnt',)] + counted
    return counted

def extract_chars_from_records(records: List[List[Union[str, int]]]):
    # Get index of the 'chars' column
    index = next((i for i,title in enumerate(records[0]) if title == 'chars'),None)
    assert index is not None, 'chars not found in list title'
    # Join all texts and count
    return ''.join(rec[index] for rec in records[1:])

## Routines to read all data records
@cache_on_latest_ts
def read_all_records() -> List[Dict[str,str]]:
    with sqlite3.connect(SQLITE_DB_MERGED) as db:
        c = db.cursor()
        c.execute(SQL_SELECT_ALL_RECORD)
        result = c.fetchall()
    result = RECORD_TITLE + result
    return result

@cache_on_latest_ts(len(POSSIBLE_MOST_COUNT))
def count_all_data(count=DEFAULT_MOST_COUNT) -> List[List[Union[str, int]]]:
    # Read all records
    recs = read_all_records()
    all_text = extract_chars_from_records(recs)
    return counting_from_str(all_text,count)   

## Read and Count data records in a range
@cache_on_latest_ts(13*4)
def read_records_in_range(year: int, month: Optional[int]=None) -> List[List[Union[str, int]]]:
    start_year, start_month = year, 1 if month is None else month
    if month is None: 
        end_year, end_month = year + 1, 1
    else:
        end_year, end_month = year, month + 1
        if end_month == 13: end_year, end_month = year + 1, 1

    start = int(datetime(start_year,start_month,1,tzinfo=TZ_GMT).timestamp())
    end = int(datetime(end_year,end_month,1,tzinfo=TZ_GMT).timestamp())

    with sqlite3.connect(SQLITE_DB_MERGED) as conn:
        c = conn.cursor()
        c.execute(SQL_SELECT_RANGED_RECORD,(start,end))
        result = c.fetchall()

    result = RECORD_TITLE + result
    return result

@cache_on_latest_ts(13*4*len(POSSIBLE_MOST_COUNT))
def count_records_in_range(year: int, month: Optional[int]=None, count: Optional[int]=DEFAULT_MOST_COUNT) -> List[List[Union[str, int]]]:
    records = read_records_in_range(year, month)
    all_text = extract_chars_from_records(records)
    return counting_from_str(all_text, count)

def read_log() -> List[str]:
    return [line.strip() for line in open(FILE_LOG_CRAWL,'r').readlines()]

# API Endpoitns
@app.get("/")
def read_root():
    return {'just to':'say hi, again.'}

@app.get("/update_server")
def update_service():
    os.system("git pull")
    return {'result':'done'}

# API Call to get all data
@app.get("/all")
@debug_gate
def get_all_records():
    return read_all_records()  

# API Call to count all data
@app.get("/all/count/{count}")
def get_all_count_most(count:int):
    if count not in POSSIBLE_MOST_COUNT:
        raise ERR_INVALID_WORD_COUNT
    return count_all_data(count)
@app.get("/all/count")
def get_all_count():
    return get_all_count_most(DEFAULT_MOST_COUNT)

# Select Data in range
@app.get("/text/{year}/{month}")
@debug_gate
def get_text_month(year: int, month: int):
    if not ( 1 <= month <= 12): raise ERR_INVALID_MONTH
    return read_records_in_range(year,month)
@app.get("/text/{year}")
@debug_gate
def get_text_year(year: int):
    return read_records_in_range(year)

# Count Data in range
@app.get("/count/{year}/{month}/top/{count}")
def get_count_month_top(year: int, month: int, count: int):
    if count not in POSSIBLE_MOST_COUNT: raise ERR_INVALID_WORD_COUNT
    if not ( 1 <= month <= 12): raise ERR_INVALID_MONTH
    return count_records_in_range(year,month,count)

@app.get("/count/{year}/top/{count}")
def get_count_year_top(year: int, count: int):
    if count not in POSSIBLE_MOST_COUNT: raise ERR_INVALID_WORD_COUNT
    return count_records_in_range(year,count=count)
    
@app.get("/count/{year}/{month}")
def get_count_month(year: int, month: int):
    return get_count_month_top(year,month,DEFAULT_MOST_COUNT)
@app.get("/count/{year}")
def get_count_year(year: int):
    return get_count_year_top(year,DEFAULT_MOST_COUNT)

# API Call of Logs
@app.get("/log/crawl")
@debug_gate
def get_log_crawl():
    logs = [ line.split(' ') for line in read_log() if 'Crawl' in line ]
    return [['time','words']] + [
        [int(datetime.strptime(' '.join((words[0], words[1])),LOG_TIME_FORMAT).timestamp()), int(words[-1])]
        for words in logs
    ]

@app.get("/log/merge")
@debug_gate
def get_log_merge():
    logs = [line.split(' ') for line in read_log() if 'Merge' in line]
    return [['time','files']] + [
        [int(datetime.strptime(' '.join((words[0], words[1])),LOG_TIME_FORMAT).timestamp()), int(words[-1])]
        for words in logs
    ]

@app.get("/log/error")
@debug_gate
def get_log_crawl():
    return [line for line in read_log() if 'ERROR' in line]
