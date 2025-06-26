from fastapi import FastAPI, HTTPException

app = FastAPI(title="Get_api", description="THis api is mainly build for testing get Endpoints. There is a data of electric products", version = '1.0.0')

laptops = {
    1: {
        "brand": "Dell",
        "model": "XPS 13",
        "processor": "Intel Core i7",
        "RAM": "16GB",
        "storage": "512GB SSD",
        "graphics": "Intel Iris Xe"
    },
    2: {
        "brand": "HP",
        "model": "Spectre x360",
        "processor": "Intel Core i5",
        "RAM": "8GB",
        "storage": "256GB SSD",
        "graphics": "Intel UHD"
    },
    3: {
        "brand": "Apple",
        "model": "MacBook Air M2",
        "processor": "Apple M2",
        "RAM": "16GB",
        "storage": "1TB SSD",
        "graphics": "Integrated 10-core GPU"
    },
    4: {
        "brand": "Lenovo",
        "model": "ThinkPad X1 Carbon",
        "processor": "Intel Core i7",
        "RAM": "32GB",
        "storage": "1TB SSD",
        "graphics": "Intel Iris Xe"
    },
    5: {
        "brand": "Asus",
        "model": "ROG Zephyrus G14",
        "processor": "AMD Ryzen 9",
        "RAM": "16GB",
        "storage": "1TB SSD",
        "graphics": "NVIDIA RTX 4060"
    }
}

@app.get('/')
def main():
    return {'message': "This is the home Page."}

@app.get("/item_search/{item_id}")
def read_item1(item_id: int):
    if item_id not in laptops.keys():
        raise HTTPException(status_code=404, detail=f"There is no item on this ID '{item_id}'")
    return {'message': f"The item founded at the index '{item_id}'", "Item": laptops[item_id]}

@app.get("/item_search")
def read_item1(item_id: int):
    if item_id not in laptops.keys():
        raise HTTPException(status_code=404, detail=f"There is no item on this ID '{item_id}'")
    return {'message': f"The item founded at the index '{item_id}'", "Item": laptops[item_id]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("get_endpoints:app", reload=True, port=8000)