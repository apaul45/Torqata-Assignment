from typing import Optional
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException, Body
from main import netflix_collection

router = APIRouter(
    tags=["netflix-data"]
)

class NetflixShow(BaseModel):
    show_id: str = Field(...)
    title: str = Field(...)
    type: str = Field(...)
    cast: str = Field(...)
    country: str = Field(...)
    date_added: str = Field(...)
    release_year: int = Field(...)
    rating: str = Field(...)
    duration: str = Field(...)
    listed_in: str = Field(...)
    description: str = Field(...)

class UpdateShowModel(BaseModel):
    show_id: Optional[str]
    title: Optional[str]
    type: Optional[str]
    cast: Optional[str]
    country: Optional[str]
    date_added: Optional[str]
    release_year: Optional[int]
    rating: Optional[str]
    duration: Optional[str]
    listed_in: Optional[str]
    description: Optional[str]

@router.get("/")
async def get_all_shows():
    #Use {_id: 0} to ignore the _id field when requesting: this is to prevent issues regarding ObjectIds in MongoDB
    shows = await netflix_collection.find({},{'_id': 0}).to_list(2)
    return shows

@router.post("/show", response_model = NetflixShow)
async def create_show(show: NetflixShow):
    show = jsonable_encoder(show) #As this show is received as a JSON string, it must be decoded into a python dict first
    new_show = await netflix_collection.insert_one(show)
    created_show = await netflix_collection.find_one({"_id": new_show.inserted_id})
    return created_show
 
@router.delete("/{show_id}")
async def delete_show(show_id: str):
    result = await netflix_collection.delete_one({"show_id": show_id})
    if result.deleted_count == 1: 
        return {"msg" : "Show has been successfully deleted!"}
    raise HTTPException(status_code = 404, detail="This show could not be deleted")

@router.put("/{show_id}")
async def update_show(show_id: str, show: UpdateShowModel = Body(...)):
    show = {k: v for k, v in show.dict().items() if v is not None}
    updated_show = await netflix_collection.update_one({"show_id": show_id}, {"$set": show})
    return {"msg": "Show successfully updated!"}