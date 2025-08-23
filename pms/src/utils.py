from fastapi import HTTPException
import json
import os

data_path = "patients.json"
counter_path = "counter.txt"

# Fallbacks in case files don't exist
if not os.path.exists(data_path):
    with open(data_path, 'w') as f:
        json.dump({}, f)

if not os.path.exists(counter_path):
    with open(counter_path, 'w') as f:
        f.write("0")

try:
    with open(data_path, 'r') as file:
        data = json.load(file)
except json.decoder.JSONDecodeError:
    data = {}

def save_data(data):
    with open(data_path, 'w') as file:
        json.dump(data, file, indent=4)

with open(counter_path, "r") as file:
    counter = int(file.read().strip())

def save_counter(counter):
    with open(counter_path, "w") as file:
        file.write(str(counter))

def check_id(id: int):
    """Check if the ID already exists in the data."""
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    
    if id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

order = {
    "Unknown": 0,
    "Amateur": 1,
    "Professional": 2,
    "Referred by a company": 3
}

def key_func(item, sort_by):
    """Helper function to extract the sorting key from the item."""
    if not sort_by:
        return item[0]
    if sort_by == 'refered_by':
        return order[item[1].get('referred_by', 'Unknown')]
    return item[1].get(sort_by, item[0])

def sort_data(sort_by, order):
    """Helper function to sort data by a specific field."""

    sorted_data = sorted(data.items(), key=lambda item: key_func(item, sort_by), reverse=(order == 'desc'))
    return sorted_data