from typing import *
from config import *
import os
from collections import Counter

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {'just to':'say hi, again.'}

@app.get("/update_server")
def update_service():
    os.system("git pull")
    return {'result':'done'}

# API Call to get all data
@app.get("/all")
def read_all_records():
    # Filter .gitkeep
    files = [ f for f in os.listdir(DIR_DB_MERGED) if f[0] != '.' ]
    return [
        { 
            'time': ts,
            'words' : open(os.path.join(DIR_DB_MERGED,ts)).readline()
        }
        for ts in files
    ]

# API Call to count all data
@app.get("/all/count")
def count_all_records():
    # Filter .gitkeep
    files = [ f for f in os.listdir(DIR_DB_MERGED) if f[0] != '.' ]
    return Counter(
        ''.join([open(os.path.join(DIR_DB_MERGED,ts)).readline() for ts in files])
    )
