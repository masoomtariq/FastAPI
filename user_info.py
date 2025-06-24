# Import required modules from FastAPI and Pydantic
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, Dict

# App description shown in Swagger UI
description = "This application specifically for practicing POST endpoints. It supports user registration, login, updation and deletion, with duplicate username handling."

# In-memory user database (key: username, value: user object)
users_db: Dict[int, Dict] = {}

# Initialize FastAPI app
app = FastAPI(title="Post_api", description=description, version="1.0.0")

# ------------------------------
# Root Route
# ------------------------------
@app.get('/')
def root_page():
    return {"message": f"Welcome to the Homepage. {description}"}

##Models
# ------------------------------
# Pydantic model for user registration
# ------------------------------
class RegisterationInfo(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    password: str\
# ------------------------------
# Pydantic model for user login
# ------------------------------
class LoginUser(BaseModel):
    username: str
    password: str


# ------------------------------
# POST route to register a user
# ------------------------------
@app.post('/register', response_model=dict)
def register_user(User: RegisterUser) -> dict:
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
# Pydantic model for user login
# ------------------------------
class LoginUser(BaseModel):
    username: str
    password: str

# ------------------------------
# POST route for login
# ------------------------------
@app.post('/login', response_model=dict)
def login_user(user: LoginUser) -> dict:

    username = user.username
    # Check if user exists
    if username not in users_db:
        raise HTTPException(status_code=401, detail="Invalid username")

    # Check password (access via attribute)
    if users_db[username].password != user.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": f"Welcome back, {username}!"}

# ------------------------------
# Uvicorn entry point for local run
# ------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("register_user:app", reload=True)
