from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware, db as pgdb
from motor.motor_asyncio import AsyncIOMotorClient

import os
from dotenv import load_dotenv
from sqlalchemy import delete, select, func, text
from shows.models import Shows as Show

app = FastAPI()

load_dotenv()

mongo_connection = os.getenv("MONGO_CONNECTION")
db = AsyncIOMotorClient(mongo_connection).torqatadb

app.add_middleware(DBSessionMiddleware, db_url=os.getenv("POSTGRES_CONNECTION"))


@app.get("/")
def root():
    type = "directors"
    value = "Tom Toelle"

    cols = [
        Show.year,
    ]

    stmt = select(cols).where(Show.year == 2012)

    row = pgdb.session.execute(stmt).first()
    return row
    return


from shows import routes as shows
from user import routes as user

app.include_router(shows.router)
app.include_router(user.router)
