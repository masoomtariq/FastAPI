from fastapi import FastAPI, HTTPException, responses
from schemas import Patient, Annotated, Field
from utils import data, save_data, counter, save_counter

app = FastAPI()

@app.post("/add")
def add_data(patient: Patient):
    global data

    id = patient.id

    data[id] = patient.model_dump(exclude=['id'])

    save_data(data)
    return responses.JSONResponse(content={"message": "Patient data added successfully", "Id": id}, status_code=201)

@app.get("/view")
def view_data():
    
    if not data:
        raise HTTPException(status_code=404, detail="No data found")
    return responses.JSONResponse(content=data)

@app.get("/view/{id}")
def view_data_by_id(id: Annotated[int, Field(..., gt=0, description="ID of the patient to view", example=1)]):
    global data

    if id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return responses.JSONResponse(content={id: data[id]})