from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Annotated

class Patient(BaseModel):
    id: int
    name: Annotated[str, Field(..., description="Full name of the patient", example="John Doe")]
    email: Annotated[EmailStr, Field(..., description="Valid email address of the patient", example="abc@gmail.com")]
    age: Annotated[int, Field(..., gt=0, le=120, description="Age must be between 1 and 120", example=30)]
    allergies: Optional[List[str]] = None