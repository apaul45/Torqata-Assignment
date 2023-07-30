from sqlmodel import select
from user.models import User, UserService
from fastapi_sqlalchemy import db as pgdb
from main import db as mdb


class SQLUserService(UserService):
    @classmethod
    async def get_user(cls, username: str):
        user = pgdb.session.execute(
            select(User).where(User.username == username)
        ).first()

        return dict(user._asdict()["User"])


class MongoUserService(UserService):
    driver = mdb.get_collection("users")

    @classmethod
    async def get_user(cls, username: str):
        return await cls.driver.find_one({"username": username})
