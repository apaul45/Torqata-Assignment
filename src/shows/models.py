from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Optional, List
from models.mongodb import PyObjectId


class Show(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    show_id: str
    position: int
    title: str
    url: str
    type: str
    rating: float
    runtime: int
    year: int
    genres: List[str]
    votes: int
    date: str
    directors: List[str]

    class Config:
        orm_mode = True


class UpdateShowModel(BaseModel):
    show_id: Optional[str]
    title: Optional[str]
    type: Optional[str]
    position: Optional[int]
    country: Optional[str]
    url: Optional[str]
    year: Optional[int]
    rating: Optional[int]
    runtime: Optional[int]
    votes: Optional[int]
    date: Optional[str]
    genres: Optional[str]

    class Config:
        orm_mode = True


class BaseShowService(ABC):
    @classmethod
    @abstractmethod
    def get_all_shows(cls):
        pass

    @classmethod
    @abstractmethod
    def create_show(cls, show: Show):
        pass

    @classmethod
    @abstractmethod
    def delete_show(cls, show_id: str):
        pass

    @classmethod
    @abstractmethod
    def update_show(cls, show_id: str, show: UpdateShowModel):
        pass

    @classmethod
    @abstractmethod
    def get_year_show_rating(cls, year: int, show_type: str = None):
        pass

    @classmethod
    @abstractmethod
    def get_year_statistics(cls, year: int = None):
        pass

    @classmethod
    @abstractmethod
    def get_director_or_genre_statistics(cls, type: str, value):
        pass
