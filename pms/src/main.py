from fastapi import FastAPI, HTTPException, responses
from schemas import Patient, Field
from typing import Annotated, Optional, Literal
from utils import data, save_data, counter, save_counter, check_id, sort_data

app = FastAPI()

@app.post("/add")
def add_data(patient: Patient):
    global data

    id = patient.id

    data[id] = patient.model_dump(exclude=['id'])

    save_data(data)
    return responses.JSONResponse(content={"message": "Patient data added successfully", "Id": id}, status_code=201)

@app.get("/view")
def view_data(sort_by: Annotated[Literal['name', 'age', 'height', 'weight', 'bmi', 'refered_by'], Field(default=None, description="Sort the data by a specific field", example="name")],
              order: Annotated[Literal['asc', 'desc'], Field(default='asc', description="Order of sorting", example="asc")]):
    
    global data
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    data = sort_data(sort_by, order)
    return data

@app.get("/view/{id}")
def view_data_by_id(id: Annotated[int, Field(..., gt=0, description="ID of the patient to view", example=1)]):
    
    global data
    check_id(id)
    
    return {id: data[id]}

@app.put("/update/{id}")
def update_data(id: Annotated[int, Field(..., gt=0, description="ID of the patient to update", examples=[1, 2])],
                patient: Annotated[Patient, Field(..., description="Updated patient data, can be one or more fields")]):
    
    global data
    check_id(id)

    patient_data = data[id]
    patient_data.update(patient.model_dump(exclude=['id']))

    data[id] = patient_data
    save_data(data)
    return responses.JSONResponse(content={"message": "Patient data updated successfully", "Id": id}, status_code=201)

@app.delete("/delete/{id}")
def delete_data(id: Annotated[int, Field(..., gt=0, description="ID of the patient to delete", example=1)]):
    
    global data
    check_id(id)

    global counter
    del data[id]
    save_data(data)
    counter -= 1
    save_counter(counter)

    return responses.JSONResponse(content={"message": "Patient data deleted successfully", "Id": id}, status_code=200) 


# Run the app using Uvicorn (used for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)