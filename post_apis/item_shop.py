# Import required libraries
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import uuid4

# Initialize FastAPI app with metadata
app = FastAPI(
    title="Item Shop",
    description="This is the API used to create and place product orders.",
    version='1.0.0'
)

# Simulated database of products
products_db = {
    1: {"name": "Book", "price": 500},
    2: {"name": "Pen", "price": 100},
    3: {"name": "Laptop", "price": 100000},
}

# In-memory list to store order summaries
orders_db = []

# Data model for each item in an order request
class OrderItem(BaseModel):
    product_id: int
    quantity: int

# Request model for placing an order
class OrderRequest(BaseModel):
    customer_id: int
    items: List[OrderItem]
    note: str = ""  # Optional note field

# Internal structure to represent an item in the final order summary
class OrderedItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    subtotal: int

# Final structure to summarize the entire order
class OrderSummary(BaseModel):
    order_id: int
    customer_id: int
    ordered_items: List[OrderedItem]
    price: int
    note: str
    timestamp: datetime

# Endpoint to place a new order
@app.post('/order/place', response_model= dict)
def place_order(order: OrderRequest) -> dict:
    total_amount = 0
    orders = []

    # Process each item in the order
    for item in order.items:
        product = products_db.get(item.product_id)
        
        # If product doesn't exist, raise error
        if not product:
            raise HTTPException(status_code=404, detail=f"Product ID {item.product_id} not found")

        # Calculate subtotal and accumulate total
        cost = product["price"] * item.quantity
        total_amount += cost

        # Append item with details
        orders.append(OrderedItem(
            product_id=item.product_id,
            product_name=product['name'],
            quantity=item.quantity,
            subtotal=cost
        ))

    # Create order summary
    order_summary = OrderSummary(
        order_id=str(uuid4()),
        customer_id=order.customer_id,
        ordered_items=orders,
        price=total_amount,
        note=order.note,
        timestamp=datetime.utcnow()
    )

    # Save to in-memory order database
    orders_db.append(order_summary)

    return {"message": "Order placed", "order": order_summary}

# Run the app using Uvicorn (used for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("item_shop:app", reload=True)