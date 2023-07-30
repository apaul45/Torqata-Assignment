from sqlalchemy import ARRAY, Column, DateTime, Integer, String, Float, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Show(Base):
    __tablename__ = "shows"
    show_id = Column(String, primary_key=True, index=True)
    position = Column(String)
    title = Column(String)
    url = Column(String)
    type = Column(String)
    rating = Column(Float)
    runtime = Column(Integer)
    year = Column(Integer)
    genres = Column(ARRAY(String))
    votes = Column(Integer)
    date = Column(DateTime(), server_default=func.now())
    directors = Column(ARRAY(String))


class User(Base):
    __tablename__ = "user"
    email = Column(String, primary_key=True)
    username = Column(String)
    passwordHash = Column(String)
