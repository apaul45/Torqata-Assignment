from pydantic import BaseModel
from main import db


class User(BaseModel):
    username: str
    email: str
    passwordHash: str


class Token(BaseModel):
    access_token: str


class UserService:
    driver = db.get_collection("users")

    @classmethod
    async def get_user(cls, username: str):
        return await cls.driver.find_one({"username": username})
