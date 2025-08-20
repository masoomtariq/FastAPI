from fastapi import HTTPException
import json

with open('/workspaces/FastAPI/pms/patients.json', 'r') as file:
    data = json.load(file)

def save_data(data):
    with open('/workspaces/FastAPI/pms/patients.json', 'w') as file:
        json.dump(data, file)

with open("/workspaces/FastAPI/pms/counter.txt", "r") as file:
    counter = int(file.read().strip())

def save_counter(counter):
    with open("/workspaces/FastAPI/pms/counter.txt", "w") as file:
        file.write(str(counter))

def check_id(id: int):
    """Check if the ID already exists in the data."""
    if id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    


