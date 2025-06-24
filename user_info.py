# Import required modules from FastAPI and Pydantic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator,EmailStr
from typing import Dict
import re

# App description shown in Swagger UI
description = "This application specifically for practicing POST endpoints. It supports user registration, login, updation and deletion, with duplicate username handling."

# In-memory user database (key: username, value: user object)
users_db: Dict[int, Dict] = {}

##Models
# ------------------------------
# Pydantic model to validate a password
# ------------------------------
class Password(BaseModel):
    password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password must contain at least one special character")
        return value
# ------------------------------
# Pydantic model for user information password excluded
# ------------------------------
class UserInfo(BaseModel):
    username: str
    email: EmailStr
    full_name: str
# ------------------------------
# Pydantic model For User Information Password included
# ------------------------------
class UserInfo_WithPass(UserInfo):
    password: Password
# ------------------------------
# Pydantic model for login Information
# ------------------------------
class LoginInfo(BaseModel):
    username: str
    password: str
# ------------------------------
# Pydantic model to change Password
# ------------------------------
class ChangePassword(LoginInfo):
    new_password: Password
    repeated_password: Password

# Initialize FastAPI app
app = FastAPI(title="Post_api", description=description, version="1.0.0")

def validate_user(login_info):

    username = login_info.username
    # Check if user exists
    if username not in users_db:
        raise HTTPException(status_code=401, detail=f"Username '{username}' not exist.")

    # Check password (access via attribute)
    if users_db[username]["password"] != login_info.password:
        raise HTTPException(status_code=401, detail="Invalid password")

# ------------------------------
# Root Route
# ------------------------------
@app.get('/')
def root_page():
    return {"message": f"Welcome to the Homepage. {description}"}

# ------------------------------
# POST route to register a user
# ------------------------------
@app.post('/register')
def register_user(user: UserInfo_WithPass):
    username = user.username

    # Check for duplicate username
    if username in users_db:
        raise HTTPException(status_code=400, detail=f"The given username '{username}' already exists.")

    # Save user (Pydantic model) to database
    users_db[username] = {"username": user.username,
                          "email": user.email,
                          "full_name": user.full_name,
                          "password": user.password.password  # get string value
                          }

    # Return success message, exclude password
    return {
        "message": f"User '{username}' registered successfully.",
        "user": {"username": user.username,
                 "email": user.email,
                 "full_name": user.full_name
                 }  # Never return passwords
    }

# ------------------------------
# POST route for login
# ------------------------------
@app.post('/login')
def login_user(login_info: LoginInfo):

    validate_user(login_info)

    return {"message": f"Welcome back, {login_info.username}!"}

# ------------------------------
# PUT route for Update Information
# ------------------------------
@app.put('/update')
def update_info(login_info: LoginInfo, user_info: UserInfo):

    validate_user(login_info)
    
    username = user_info.username
    
    del users_db[login_info.username]

    users_db[username] = {"username": username,
                          "email": user_info.email,
                          "full_name": user_info.full_name,
                          "password": login_info.password}
    
    return {'message': "The user's information updated successfully!."}

# ------------------------------
# PUT route for change Password
# ------------------------------
@app.put('/change_password')
def change_password(user_info: ChangePassword):

    validate_user(user_info)
    if user_info.new_password != user_info.repeated_password:
        raise HTTPException(status_code=400, detail= "The Entered password must be match")
    
    users_db[user_info.username]["password"] = user_info.new_password

    return {"message": "The password has been changed successfully."}
# ------------------------------
# DELETE route to delete user
# ------------------------------
@app.delete('/delete')
def delete_user(login_info: LoginInfo):

    validate_user(login_info)

    username = login_info.username

    del users_db[username]

    return {"message": f"The user '{username}' has been deleted."}
    
# ------------------------------
# Uvicorn entry point for local run
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("user_info:app", reload=True)
