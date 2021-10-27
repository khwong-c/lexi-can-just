from typing import *
from config import *
import os
import glob
from collections import Counter
from functools import lru_cache

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware)

# Getting the name of the latest file as signature
def get_latest_file() -> str:
    return max(glob.iglob(DIR_DB_MERGED),key=os.path.getctime)

def get_whole_file_list() -> List[str]:
    # Filter .gitkeep
    return [ f for f in os.listdir(DIR_DB_MERGED) if f[0] != '.' ]

## Routines to read all data records
@lru_cache(2)
def read_all_records_core(latest_file: str) -> List[Dict[str,str]]:
    files = get_whole_file_list()
    return [
        { 
            'time': ts,
            'words' : open(os.path.join(DIR_DB_MERGED,ts)).readline()
        }
        for ts in files
    ]

def read_all_records() -> List[Dict[str,str]]:
    # Cached core function + Signature
    return read_all_records_core(get_latest_file())
    
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
def count_all_records():
    records = read_all_records()
    return Counter(
        ''.join([rec['words'] for rec in records])
    )
