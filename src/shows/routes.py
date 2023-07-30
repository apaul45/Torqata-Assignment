from typing import Optional
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, HTTPException, Body
from user.routes import get_current_user
from shows.services.mongodb import ShowService
from shows.models import Show, UpdateShowModel

router = APIRouter(tags=["shows"])


@router.get("/shows")
async def get_all_shows(service: ShowService = Depends(ShowService)):
    shows = await service.get_all_shows()
    return shows


@router.post("/show", response_model=Show)
async def create_show(
    show: Show,
    user=Depends(get_current_user),
    service: ShowService = Depends(ShowService),
):
    show = jsonable_encoder(
        show
    )  # As this show is received as a JSON string, it must be decoded into a python dict first

    return await service.create_show(show)


@router.delete("/{show_id}")
async def delete_show(
    show_id: str,
    user=Depends(get_current_user),
    service: ShowService = Depends(ShowService),
):
    result = await service.delete_show(show_id)

    if not result:
        raise HTTPException(status_code=404, detail="This show could not be deleted")

    return show_id


@router.put("/{show_id}")
async def update_show(
    show_id: str,
    show: UpdateShowModel = Body(...),
    user=Depends(get_current_user),
    service: ShowService = Depends(ShowService),
):
    result = await service.update_show(show_id, show)

    if not result:
        raise HTTPException(status_code=304)

    return show


# Aggregation


# async def get_result(stage_list):
#     shows = await imdb_collection.aggregate(stage_list).to_list(length=None)
#     result = []
#     for show in shows:
#         if show["_id"] == None or show["_id"] == "missing":
#             del show["_id"]
#         result.append(show)
#     return result


@router.get(
    "/rating/type/{year}",
    response_description="Returns the average rating for either a certain type of shows or every show in a given year",
)
async def year_show_rating(
    year: int,
    show_type: Optional[str] = "$type",
    service: ShowService = Depends(ShowService),
):
    return await service.get_year_show_rating(year, show_type)


@router.get(
    "/yearly",
    response_description="Returns average runtime and ratings for each year or a given year",
)
async def year_statistics(
    year: Optional[int] = None,
    service: ShowService = Depends(ShowService),
):
    return await service.get_year_statistics(year)


@router.get("/rating/{director}")
async def director_statistics(
    director: str,
    service: ShowService = Depends(ShowService),
):
    return await service.get_director_or_genre_statistics("directors", director)


@router.get("/rating/{genre}")
async def genre_statistics(
    genre: str,
    service: ShowService = Depends(ShowService),
):
    return await service.get_director_or_genre_statistics("genres", genre)
