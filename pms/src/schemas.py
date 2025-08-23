from pydantic import BaseModel, Field, EmailStr, computed_field, model_validator
from typing import List, Annotated, ClassVar
from utils import counter, save_counter

class Patient(BaseModel):
    name: Annotated[str, Field(..., max_length=50, description="Full name of the patient", example="John Doe")]
    email: Annotated[EmailStr, Field(..., description="Valid email address of the patient", example="abc@gmail.com")]
    phone_no: Annotated[str, Field(..., description="Phone number of the patient", example="+1234567890")]
    age: Annotated[int, Field(..., gt=0, le=120, description="Age must be between 1 and 120", example=30)]
    height: Annotated[float, Field(..., gt=0, description="Height in meters", example=1.75)]
    weight: Annotated[float, Field(..., gt=0, description="Weight in kilograms", example=70.5)]
    allergies: Annotated[List[str], Field(default=None, max_length=5, description="List of allergies", example=["Peanuts", "Penicillin"])]

    _emails: ClassVar[set[EmailStr]] = set()  # Class variable to track unique emails
    _phones: ClassVar[set[str]] = set()  # Class variable to track unique phone numbers

    @computed_field
    @property
    def id(self) -> int:
        """Automatically generated ID for the patient."""
        global counter
        counter += 1
        save_counter(counter)
        return counter

    @computed_field
    @property
    def bmi(self) -> float:
        """Calculate Body Mass Index (BMI) based on height and weight."""
        if self.height <= 0 and self.weight <= 0:
            raise ValueError("Height and weight must be greater than zero to calculate BMI.")
        return round(self.weight / (self.height ** 2), 2)
    
    @computed_field
    @property
    def bmi_class(self) -> str:
        """Determine BMI classification."""
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal weight"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obesity"
        
    @computed_field
    @property
    def referred_by(self) -> str:
        """Determine whether the patient is referred by some company based on email domain."""

        common_domains = ["gmail.com", "yahoo.com", "hotmail.com"]
        special_domains = ['the.akdn', 'parco.com.pk', 'ke.com.pk', 'bop.com.pk']
        domain = self.email.split('@')[-1]

        if domain in common_domains:
            return "Amateur"
        if domain in special_domains:
            return "Referred by a company"
        return "Professional"
    
    @model_validator(mode='after')
    def check_uniqueness(self):

        # Email uniqueness
        if self.email in Patient._emails:
            raise ValueError(f"Email '{self.email}' already exists")

        # Phone uniqueness
        if self.phone_no in Patient._phones:
            raise ValueError(f"Phone_No '{self.phone_no}' already exists")

        # Only update sets if everything is unique
        Patient._emails.add(self.email)
        Patient._phones.add(self.phone_no)

        return self