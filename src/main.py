from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

import os
from dotenv import load_dotenv # Will look for .env file, if not found then vars in host env
from sqlmodel import create_engine

app = FastAPI()

load_dotenv()

mongo_connection = os.getenv("MONGO_CONNECTION")
db = AsyncIOMotorClient(mongo_connection).torqatadb

pg_engine = create_engine(os.getenv("POSTGRES_CONNECTION"))


@app.get("/")
def root():
    return "Welcome to my backend"


from shows import routes as shows
from user import routes as user

app.include_router(shows.router)
app.include_router(user.router)
