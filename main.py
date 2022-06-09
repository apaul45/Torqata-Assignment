import asyncio
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()
connection_url = "mongodb+srv://apaul45:password123apaul@cluster0.qr58u.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
db = AsyncIOMotorClient(connection_url).torqatadb
db.get_io_loop = asyncio.get_event_loop
imdb_collection = db.get_collection("imdb_shows")
user_collection = db.get_collection("users")

@app.get("/")
def root():
    return {"msg": "Welcome to my backend"}

import crud
import aggregation
import user

app.include_router(crud.router)
app.include_router(aggregation.router)
app.include_router(user.router)