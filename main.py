# main.py

from fastapi import FastAPI

# Step 1: Create our "waiter"
app = FastAPI()

# Step 2: Define a "dish" (endpoint)
@app.get("/")
def home():
    return {"message": "Hello! Dog vs Cat API is awake 😺🐶"}
