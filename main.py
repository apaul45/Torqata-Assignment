from fastapi import FastAPI
import motor.motor_asyncio 

app = FastAPI()
db = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017").torqatadb
imdb_collection = db.get_collection("imdb_shows")
user_collection = db.get_collection("users")

import crud
import aggregation
import user

app.include_router(crud.router)
app.include_router(aggregation.router)
app.include_router(user.router)