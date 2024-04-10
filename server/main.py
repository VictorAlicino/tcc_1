"""Main module"""
from fastapi import FastAPI, HTTPException
app = FastAPI()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"payload": "Hello World"}


@app.get("hello/{name}")
async def say_hello(name: str):
    """Say hello to the user"""
    return {"message": f"Hello {name}"}
