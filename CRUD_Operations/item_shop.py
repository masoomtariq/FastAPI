from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

# Pydantic model for a product
class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True

# In-memory 'database' using dictionary {item_id: Product}
item_db: Dict[int, Product] = {}

# App metadata
description = "In the Application you can search, upload, update and delete the Item's data."
app = FastAPI(title="Item Store", description=description, version='1.0.0')


@app.get('/')
def root_page():
    # Welcome message with app description
    return {"message": f"Welcome to the Item Store. {description}"}


@app.get('/items')
def get_all_item():
    # Return all items or raise error if DB is empty
    if not item_db:
        raise HTTPException(status_code=404, detail="There is no item available.")
    return {"Items": item_db}


@app.get('/item/{item_id}')
def search_item(item_id: int):
    # Search item by ID using path parameter
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail=f"The item ID '{item_id}' was not found.")
    return {"message": "Item found", "Item": item_db[item_id]}


@app.get('/search')
def get_item(name: str):
    # Search item(s) by name (case-insensitive)
    results = {id: item for id, item in item_db.items() if item.name.lower() == name.lower()}
    if not results:
        raise HTTPException(status_code=404, detail=f"No item found with the name '{name}'.")
    return {"Results": results}


@app.post('/item')
def add_item(item: Product):
    # Add a new item with auto-incremented ID
    item_id = len(item_db) + 1
    item_db[item_id] = item
    return {'id': item_id, "Item": item}


@app.put('/item/{item_id}')
def update_item(item_id: int, item: Product):
    # Update item by ID if it exists
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    item_db[item_id] = item
    return {"message": "Item updated successfully", "Item": item}


@app.delete('/item/{item_id}')
def delete_item(item_id: int):
    # Delete item by ID if it exists
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del item_db[item_id]
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:item_shop", reload=True)