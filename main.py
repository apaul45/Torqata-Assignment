from fastapi import FastAPI
import motor.motor_asyncio 

app = FastAPI()
db = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017").torqatadb
imdb_collection = db.get_collection("imdb_shows")

import crud
import aggregation

app.include_router(crud.router)
app.include_router(aggregation.router)