import csv
from datetime import datetime
from typing import List
from fastapi import FastAPI, UploadFile, File
from .routers import files_process, auth

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to test task API"}

app.include_router(files_process.router)
app.include_router(auth.router)