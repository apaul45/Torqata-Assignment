from abc import ABC, abstractmethod
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from main import db


class User(SQLModel, table=True):
    email: str = Field(default=None, primary_key=True)
    username: str
    passwordHash: str


class Token(BaseModel):
    access_token: str


class UserService(ABC):
    @classmethod
    @abstractmethod
    def get_user(cls, username: str):
        pass
