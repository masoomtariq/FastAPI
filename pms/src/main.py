from fastapi import FastAPI, HTTPException, responses
from schemas import Patient, Annotated, Field
from utils import data, save_data, counter, save_counter, check_id

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
    check_id(id)
    
    return responses.JSONResponse(content={id: data[id]})

@app.put("/update/{id}")
def update_data(id: Annotated[int, Field(..., gt=0, description="ID of the patient to update", examples=[1, 2])],
                patient: Annotated[Patient, Field(..., description="Updated patient data, can be one or more fields")]):
    
    global data
    check_id(id)

    patient_data = data[id]
    patient_data.update(patient.model_dump(exclude_unset=True))

    for key, value in patient.model_dump(exclude_unset=True).items():