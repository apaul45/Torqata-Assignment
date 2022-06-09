from fastapi import APIRouter, Depends
from main import imdb_collection
from pprint import pprint
from typing import Optional
from user import get_current_user

router = APIRouter(
    tags=["aggregation-routes"]
)

async def get_result(stage_list):
    shows = await imdb_collection.aggregate(stage_list).to_list(length=None)
    result = []
    for show in shows: 
        pprint(show)
        if show["_id"] == None or show["_id"] == "missing":
            del show["_id"]
        result.append(show)
    return result

async def type_query_helper(query_type: str, query_operation: object, id: Optional[str] = None):
    match_stage = {
        "$match": {
            query_type: query_operation
        }
    }
    group_id = {
        "$type": '$' + id
    } if id else "$type"
    
    group_stage = {
        "$group": {
            "_id": group_id,
            "average": {
                "$avg": "$rating"
            }
        }
    }
    return await get_result([match_stage, group_stage])

#This request returns the average rating for either a certain type of show  or every show with a certain number of votes
@router.get("/rating/type/{votes}", response_description="Returns the average rating for a certain type of show with a certain number of votes")
async def type_vote_rating(votes: int, type: Optional[str] = None, user = Depends(get_current_user)):
    return await type_query_helper("votes", {"$gte": votes}, type)

#This request returns the average rating of either a certain type of show or every show in a specific year
@router.get("/rating/type/{year}", response_description="Returns the average rating for either a certain type of shows or every show in a given year")
async def type_year_rating(year: int, type: Optional[str] = None, user = Depends(get_current_user)):
    return await type_query_helper("year", {"$eq": year}, type)

#This request returns the average runtime and ratings of shows in either a given year or all years in a sorted list
@router.get("/yearly", response_description="Returns average runtime and ratings for each year or a given year")
async def year_statistics(year: Optional[int] = None, user = Depends(get_current_user)): 
    yr = {
        "$year": '$' + str(year)
    } if year else "$year"

    show_group = {
        "$group": {
            "_id": yr,
            "averageRating": {
                "$avg": "$runtime"
            },
            "averageRuntime": {
                "$avg" : "$rating"
            }
        }
    }
    sort_groups = {
        "$sort": {
            "_id": 1
        }
    }
    return await get_result([show_group, sort_groups])

@router.get("/rating/{director}")
async def director_statistics(director: str, user = Depends(get_current_user)):
    match_director = {
        "$match": {
            "directors": {
                "$eq": director
            }
        }
    }
    group_stage = {
        "$group": {
            "_id": "$title",
            "averageRating": {
                "$avg": "$rating"
            }
        }
    }
    return await get_result([match_director, group_stage])