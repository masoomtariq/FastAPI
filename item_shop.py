from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

# Pydantic model for a product
class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True

# In-memory 'database'
item_db: Dict[int, Product] = {}

description = "In the Application you can search, upload, update and delete the Item's data."

app = FastAPI(title="Item Store", description=description, version='1.0.0')

@app.get('/')
def root_page():
    return {"message": f"Welcome to the Item Store. {description}"}

@app.get('/items', response_model= Dict)
def get_all_item():
    if not item_db:
        raise HTTPException(status_code=403, detail="There is no item")
    return {"Items": item_db}

@app.get('/item')
def search_item(item_id: int):
    if item_id not in item_db:
        raise HTTPException(status_code=401, detail=f"The Given item id '{item_id}' not found.")
    
    item = item_db.get(item_id)

    return {"message": "Your requested item has been found", "Item": item}

@app.get('/search')
def get_item(name: str):
    results = {id: item for id, item in item_db.items() if item.name.lower() == name.lower()}
    if not results:
        raise HTTPException(status_code=404, detail=f"No Item Found on this name '{name}'")
    return {"Results": results}

@app.post('/item', response_model= Dict)
def add_item(item: Product) -> Dict:
    item_id = len(item_db)+1
    item_db[item_id] = item
    return {'id': item_id, "Item": item}

@app.put('/item')
def update_item(item_id: int, item: Product):
    if item_id not in item_db:
        raise HTTPException(404, detail="Item not found")

    item_db[item_id] = item

    return {"message": "Item updated", "Item": item}

@app.delete('/delitem')
def delete_item(item_id: int):
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del item_db[item_id]

    return {"message": "Item deleted successfully"}