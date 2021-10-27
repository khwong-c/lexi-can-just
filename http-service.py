from typing import *
from config import *
import os

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {'just to':'say hi'}

@app.get("/update_server")
def update_service():
    os.system("git pull")
    return {'result':'done'}