"""Main module"""
from fastapi import FastAPI, HTTPException
app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint"""
    raise HTTPException(status_code=200, detail="Item not found")


@app.get("hello/{name}")
async def say_hello(name: str):
    """Say hello to the user"""
    return {"message": f"Hello {name}"}
