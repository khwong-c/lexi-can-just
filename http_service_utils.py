from typing import *
import os
import glob
from config import *
from functools import wraps
from time import perf_counter

# Getting the name of the latest file as signature
ALL_FILES = os.path.join(DIR_DB_MERGED,'*')

def benchmark(func):
    @wraps(func)
    def timed_function(*args,**kwargs):
        t0 = perf_counter()
        result = func(*args,**kwargs)
        t1 = perf_counter()
        print(t1-t0)
        return result
    return timed_function

def get_latest_file() -> str:
    files = [f for f in os.scandir(DIR_DB_MERGED)]
    return max(files,key=lambda f:f.stat().st_ctime).name

def cache_on_latest_file(func):
    @wraps(func)
    def cached_function(*args,**kwargs):
        sig = cached_function.signature
        latest_name = get_latest_file()
        if sig is None or sig != latest_name:
            cached_function.signature = latest_name
            cached_function.cached_result = func(*args,**kwargs)
        return cached_function.cached_result
    cached_function.signature = None
    cached_function.cached_result = None
    return cached_function

@cache_on_latest_file
def get_whole_file_list() -> List[str]:
    # Filter .gitkeep
    return [f.name for f in os.scandir(DIR_DB_MERGED) if f.is_file() and not f.name.startswith('.')]
