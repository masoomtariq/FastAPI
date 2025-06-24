# Import required modules from FastAPI and Pydantic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

# App description shown in Swagger UI
description = "This application specifically for practicing POST endpoints. It supports user registration, login, updation and deletion, with duplicate username handling."

# In-memory user database (key: username, value: user object)
users_db: Dict[int, Dict] = {}

##Models
# ------------------------------
# Pydantic model for user registration information
# ------------------------------
class RegisterationInfo(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str\
# ------------------------------
# Pydantic model for login Information
# ------------------------------
class LoginInfo(BaseModel):
    username: str
    password: str

# Initialize FastAPI app
app = FastAPI(title="Post_api", description=description, version="1.0.0")

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
def register_user(User: RegisterationInfo):
    username = User.username

    # Check for duplicate username
    if username in users_db:
        raise HTTPException(status_code=400, detail=f"The given username '{username}' already exists.")

    # Save user (Pydantic model) to database
    users_db[username] = User

    # Return success message, exclude password
    return {
        "message": f"User '{username}' registered successfully.",
        "user": User.model_dump(exclude={"password"})  # Never return passwords
    }

# ------------------------------
# POST route for login
# ------------------------------
@app.post('/login')
def login_user(login_info: LoginInfo):

    username = login_info.username
    # Check if user exists
    if username not in users_db:
        raise HTTPException(status_code=401, detail=f"Username '{username}' not exist.")

    # Check password (access via attribute)
    if users_db[username].password != login_info.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": f"Welcome back, {username}!"}

# ------------------------------
# PUT route for Update Information
# ------------------------------
@app.put('/update')
def update_info(username: str, user: LoginInfo):
    if username not in users_db:
        raise HTTPException(status_code=404, detail=f"Username '{username}' not exist.")
    
    # Check password (access via attribute)
    if users_db[username].password != login_info.password:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    users_db[username] = user
    return {'message': "The user's information updated successfully!."}
    
# ------------------------------
# Uvicorn entry point for local run
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("register_user:app", reload=True)
