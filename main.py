from fastapi import FastAPI
import motor.motor_asyncio 

app = FastAPI()
db = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017").torqatadb
netflix_collection = db.get_collection("netflix_data")

from db import router
app.include_router(router)