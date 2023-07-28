from pydantic import BaseModel, Field
from typing import Optional, List
from models import PyObjectId


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
