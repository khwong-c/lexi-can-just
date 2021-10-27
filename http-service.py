from typing import *
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {'just to':'say hi'}