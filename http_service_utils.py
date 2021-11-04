from typing import *
import os
from config import *
from functools import wraps
from functools import lru_cache
from time import perf_counter, monotonic
import sqlite3
from sql_queries import *

def benchmark(func):
    @wraps(func)
    def timed_function(*args,**kwargs):
        t0 = perf_counter()
        result = func(*args,**kwargs)
        t1 = perf_counter()
        print(t1-t0)
        return result
    return timed_function

def timed_cache(TTL=20):

    def internal_deco(func):
        @wraps(func)
        def time_cached_function(*args,**kwargs):
            sig = time_cached_function.signature
            latest_sig = int(monotonic())
            if sig + time_cached_function.TTL < latest_sig:
                time_cached_function.signature = latest_sig
                time_cached_function.result = func(*args,**kwargs)
            return time_cached_function.result
        time_cached_function.signature = -TTL - 1
        time_cached_function.TTL = TTL
        
        return time_cached_function
    
    if callable(TTL):
        func, TTL = TTL, 20
        return internal_deco(func)
    else:
        return internal_deco

@timed_cache(TS_CACHE_TTL)
def get_latest_sql_ts() -> int:
    with sqlite3.connect(SQLITE_DB_MERGED) as conn:
        c = conn.cursor()
        c.execute(SQL_GET_LATEST_TIMESTAMP)
        result = c.fetchone()
        result = 0 if result is None else result[0]
        return result

def cache_on_latest_ts(cache_size=1):
    
    def internal_deco(func):
        @wraps(func)
        def filename_cached_function(*args,**kwargs):
            sig = filename_cached_function.signature
            latest_sig = get_latest_sql_ts()
            if sig is None or sig != latest_sig:
                filename_cached_function.signature = latest_sig
                filename_cached_function.cached_function.cache_clear()
            return filename_cached_function.cached_function(*args,**kwargs)
        filename_cached_function.signature = None
        filename_cached_function.cached_function = lru_cache(maxsize=cache_size)(func)
        return filename_cached_function
    
    if callable(cache_size):
        func, cache_size = cache_size, 1
        return internal_deco(func)
    else:
        return internal_deco

def debug_gate(func): 
    @wraps(func)
    def internal_func(*args,**kwargs):
        if DEBUG == '':
            return {'debug_function':True}
        else:
            return func(*args,**kwargs)
    return internal_func