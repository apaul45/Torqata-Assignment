from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

db = AsyncIOMotorClient("mongodb://localhost:27017").torqatadb
imdb_collection = db.get_collection("imdb_shows")
user_collection = db.get_collection("users")

@app.get("/")
def root():
    return {"msg": "Welcome to my backend"}

from db_collections import crud, aggregation, user
app.include_router(crud.router)
app.include_router(aggregation.router)
app.include_router(user.router)