from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Item Store", description="In this application there a crud operations performs on the item.", version='1.0.0')

@app.get('/')
def root_page():
    return {"message": "Welcome to the "}