from fastapi import APIRouter, Depends
import sys
sys.path.insert(0,"..")
from main import imdb_collection
from typing import Optional
from db_collections.user import get_current_user

router = APIRouter(
    tags=["aggregation-routes"]
)

async def get_result(stage_list):
    shows = await imdb_collection.aggregate(stage_list).to_list(length=None)
    result = []
    for show in shows: 
        if show["_id"] == None or show["_id"] == "missing":
            del show["_id"]
        result.append(show)
    return result

async def type_query_helper(query_type: str, query_operation: object, show_type: Optional[str] = None):
    #Use the match stage to filter out documents that satisfy the passed in query operation
    #Include a type query in the match stage if a type is specified; else group by type in group stage
    match_stage = {
        "$match": {
            query_type: query_operation
        }
    } if not show_type else {
        "$match": {
            query_type: query_operation,
            "type": show_type
        }
    }
    #Group the matched documents by type if no specific type given, else return the average rating of this type
    group_stage = {
        "$group": {
            "_id": "$type" if not show_type else None,
            "averageRating": {
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
async def type_year_rating(year: int, type: Optional[str] = "$type", user = Depends(get_current_user)):
    return await type_query_helper("year", {"$eq": year}, type)

#This request returns the average runtime and ratings of shows in either a given year or all years in a sorted list
@router.get("/yearly", response_description="Returns average runtime and ratings for each year or a given year")
async def year_statistics(year: Optional[int] = None, user = Depends(get_current_user)): 
    match_stage = {
        "$match": {
            "year": {
                "$eq": year
            }
        }
    } if year else None #Use match stage to filter out documents w/specific year if passed in

    #Group documents by year if no specific year given, else calculate the stats for this group only
    show_group = {
        "$group": {
            "_id": "$year" if not match_stage else None, 
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
            "_id": 1 #Sort in asc ordr
        }
    }

    aggregation_pipeline = [show_group, sort_groups]
    #Finally, only include match stage if it's defined
    if match_stage: 
        aggregation_pipeline.insert(0, match_stage)

    return await get_result(aggregation_pipeline)

async def director_genre_helper(field: str, value: str):
    match_stage = {
        "$match": {
            field: value
        }
    }
    group_stage = {
        "$group": {
            "_id": None,
            "averageRating": {
                "$avg": "$rating"
            }
        }
    }
    return await get_result([match_stage, group_stage])

@router.get("/rating/{director}")
async def director_statistics(director: str, user = Depends(get_current_user)):
    return await director_genre_helper("directors", director)

@router.get("/rating/{genre}")
async def genre_statistics(genre: str, user = Depends(get_current_user)):
    return await director_genre_helper("genres", genre)
