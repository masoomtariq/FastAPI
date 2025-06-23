from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

item_db: dict[int, dict] = {}

description = "In the Application you can search, upload, update and delete the Item's data."

app = FastAPI(title="Item Store", description=description, version='1.0.0')

@app.get('/')
def root_page():
    return {"message": f"Welcome to the Item Store. {description}"}

@app.get('/search')
def search_item(item_id: int):
    if item_id not in item_db:
        raise HTTPException(status_code=401, detail=f"The Given item id '{item_id}' not found.")
    
    item = item_db.get(item_id)

    return {"message": "Your requested item has been found", "Item": item}

@app.get('/search')
