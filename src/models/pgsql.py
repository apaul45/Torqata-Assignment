from sqlalchemy import ARRAY, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Show(Base):
    __tablename__ = "shows"
    show_id = Column(Integer, primary_key=True, index=True)
    position = Column(String)
    title = Column(String)
    url = Column(String)
    type = Column(String)
    rating = Column(Float)
    runtime = Column(Integer)
    year = Column(Integer)
    genres = Column(ARRAY(String))
    votes = Column(Integer)
    date = Column(Integer)
    directors = Column(ARRAY(String))


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
