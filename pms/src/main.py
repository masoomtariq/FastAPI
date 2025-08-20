from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/view"):
def view():

    