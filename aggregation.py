from fastapi import APIRouter, Depends
from main import imdb_collection
from pprint import pprint
from typing import Optional
from user import get_current_user

router = APIRouter(
    tags=["aggregation-routes"]
)

def match_stage(attr: str, operator: str, value):
    return  {
        "$match": {
            attr: {
                operator: value
            }
        }
    }

def average_rating_stage(attr: str, group:str):
    return {
        "$group": {
            "_id": {
                attr: group
            },
            "average": {
                "$avg": "$rating"
            }
        }
    }

async def get_result(stage_list):
    shows = await imdb_collection.aggregate(stage_list).to_list(length=None)
    result = []
    for show in shows: 
        pprint(show)
        if show["_id"] == None or show["_id"] == "missing":
            del show["_id"]
        result.append(show)
    return result

#This request returns the average rating for a certain type of show with a certain number of votes
@router.get("/rating/type/{votes}")
async def type_vote_rating(type: str, votes: int, user = Depends(get_current_user)):
    movie_type = '$' + type
    show_match_votes = match_stage("votes", "$gte", votes)
    show_group_type = average_rating_stage("$type", movie_type)
    return await get_result([show_match_votes, show_group_type])

#This request returns the average rating of a certain type of show in a specific year
@router.get("/rating/type/{year}")
async def type_year_rating(type: str, year: int, user = Depends(get_current_user)):
    movie_type = '$' + type
    show_match_votes = match_stage("year", "$eq", year)
    show_group = average_rating_stage('$type', movie_type)
    return await get_result([show_match_votes, show_group])

#This request returns the average runtime and ratings of shows in either a given year
#Or all years
@router.get("/yearly")
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
    return await get_result([show_group])
