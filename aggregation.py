from fastapi import APIRouter
from main import imdb_collection
from pprint import pprint

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
        result.append(show)
    return result

#This request returns the average rating for a certain type of show with a certain number of votes
@router.get("/rating/type/{votes}")
async def type_vote_rating(type: str, votes: int):
    movie_type = '$' + type
    show_match_votes = match_stage("votes", "$gte", votes)
    show_group_type = average_rating_stage("$type", movie_type)
    return await get_result([show_match_votes, show_group_type])

#This request returns the average rating of a certain type of show in a specific year
@router.get("/rating/type/{year}")
async def type_year_rating(type: str, year: int):
    movie_type = '$' + type
    show_match_votes = match_stage("year", "$eq", year)
    show_group = average_rating_stage('$type', movie_type)
    return await get_result([show_match_votes, show_group])

#This request returns the average runtime of shows in a given year
@router.get("/runtime/{year}")
async def year_runtime(year: int): 
    yr = '$' + str(year)
    show_group = {
        "$group": {
            "_id": {
                "$year": yr
            },
            "average": {
                "$avg": "$runtime"
            }
        }
    }
    return await get_result([show_group])

#This request returns a list of average ratings by year
@router.get("/ratings")
async def year_ratings():
    show_group = {
        "$group": {
            "_id": "$year",
            "averageRating": {
                "$avg": "$rating"
            }
        }
    }
    return await get_result([show_group])

#This request returns a list of average runtime by year
@router.get("/runtime")
async def year_runtime():
    show_group = {
        "$group": {
            "_id": "$year",
            "averageRuntime": {
                "$avg": "$runtime"
            }
        }
    }
    return await get_result([show_group])