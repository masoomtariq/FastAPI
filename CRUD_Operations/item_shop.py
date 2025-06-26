from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict

# Pydantic model for a Item
class Item(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True

# Pydantic model for a Product (alias for Item)
class Item_with_id(Item):
    id: int

# In-memory 'database' using dictionary {item_id: Product}
item_db: Dict[int, Item] = {}

def validate_item_by_id(item_id: int):
    # Validate item ID before searching or updating
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="The item ID '{item_id}' was not found.")

def validate_item_by_name_price(item: Item):
    # Validate item data before adding or updating
    if item.price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative.")
    if not item.name:
        raise HTTPException(status_code=400, detail="Item name cannot be empty.")

# App metadata
description = "In the Application you can search, upload, update and delete the Item's data."
app = FastAPI(title="Item Store", description=description, version='1.0.0')

@app.get('/')
def root_page():
    # Welcome message with app description
    return {"message": f"Welcome to the Item Store. {description}"}

@app.get('/all_items', response_model=list[Item_with_id])
def get_all_item():
    # Return all items or raise error if DB is empty
    if not item_db:
        raise HTTPException(status_code=404, detail="There is no item available.")
    # Return all items with IDs
    # Using list comprehension to add IDs to each item
    # This is done to ensure the response model includes the ID field
    # as required by the Item_with_id model
    return [{"Id": item_id, **item} for item_id, item in item_db.items()]


@app.get('/item/{item_id}', response_model=list[Item_with_id])
def search_item(item_id: int):
    # Validate item ID before searching
    validate_item_by_id(item_id)
    # Check if item is in stock
    if not item_db[item_id].in_stock:
        raise HTTPException(status_code=404, detail=f"The item ID '{item_id}' is not in stock.")
    
    return [{"message": "Item found", "Item": item_id, **item_db[item_id]}]


@app.get('/search/{name}', response_model=list[Item_with_id])
def get_item(name: str):
    
    # Search item(s) by name (case-insensitive)
    results = {id: item for id, item in item_db.items() if item.name.lower() == name.lower()}
    if not results:
        raise HTTPException(status_code=404, detail=f"No item found with the name '{name}'.")
    # Return results with IDs
    return [{"Id": id, **item} for id, item in results.items()]


@app.post('/item')
def add_item(item: Item):
    # Add a new item with auto-incremented ID
    item_id = max(item_db.keys(), default=0) + 1  # Get the next ID

    validate_item(item)  # Validate item data before adding

    # Add item to the database
    item_db[item_id] = item
    return {"message": "Item added successfully", "Item": {"Id": item_id, **item.dict()}}


@app.put('/update_item/{item_id}')
def update_item(item_id: int, item: Item):
    # Update item by ID if it exists
    if item_id not in item_db:
        raise HTTPException(status_code=404, detail="Item not found")
    
    validate_item(item)  # Validate item data before updating
    # Update item in the database
    item_db[item_id] = item
    return {"message": "Item updated successfully", "Item": item}


@app.delete('/item/{item_id}')
def delete_item(item_id: int):
    # Delete item by ID if it exists
    
    del item_db[item_id]
    return {"message": "Item deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("item_shop:app", reload=True)