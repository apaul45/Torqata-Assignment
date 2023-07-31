from sqlmodel import select, Session
from user.models import User, UserService
from main import pg_engine, db as mdb


class SQLUserService(UserService):
    session = Session(pg_engine)

    @classmethod
    async def get_user(cls, username: str):
        user = cls.session.execute(
            select(User).where(User.username == username)
        ).first()

        return dict(user._asdict()["User"])


class MongoUserService(UserService):
    driver = mdb.get_collection("users")

    @classmethod
    async def get_user(cls, username: str):
        return await cls.driver.find_one({"username": username})
