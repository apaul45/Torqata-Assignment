from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db as pgdb
from motor.motor_asyncio import AsyncIOMotorClient

import os
from dotenv import load_dotenv
from sqlalchemy import delete, select, func, text
from models.pgsql import Show

app = FastAPI()

load_dotenv()

mongo_connection = os.getenv("MONGO_CONNECTION")
db = AsyncIOMotorClient(mongo_connection).torqatadb

app.add_middleware(DBSessionMiddleware, db_url=os.getenv("POSTGRES_CONNECTION"))


@app.get("/")
def root():
    # year = None
    # show_type = None

    # cols = [
    #     Show.year,
    #     func.avg(Show.runtime).label("averageRuntime"),
    #     func.avg(Show.rating).label("averageRating"),
    # ]

    # show_id = "tt0065620"
    # stmt = delete(Show).where(Show.show_id == show_id)
    # print(stmt)
    # pgdb.session.execute(stmt)
    # pgdb.session.commit()

    # row = pgdb.session.execute(select(Show).where(Show.year == 2012)).first()
    # return row
    return


from shows import routes as shows
from user import routes as user

app.include_router(shows.router)
app.include_router(user.router)
