from main import db
from shows.models import Show, UpdateShowModel


class ShowService:
    driver = db.get_collection("imdb_shows")

    @classmethod
    async def get_all_shows(cls):
        shows = await cls.driver.find({}).to_list(length=None)
        return shows

    @classmethod
    async def create_show(cls, show: Show):
        new_show = await cls.driver.insert_one(show)
        created_show = await cls.driver.find_one({"_id": new_show.inserted_id})

        return created_show

    @classmethod
    async def delete_show(cls, show_id: str) -> bool:
        result = await cls.driver.delete_one({"show_id": show_id})

        return result.deleted_count == 1

    @classmethod
    async def update_show(cls, show_id: str, show: UpdateShowModel) -> bool:
        result = await cls.driver.update_one({"show_id": show_id}, {"$set": show})

        return result.modified_count == 1

    ## Aggregation queries

    @classmethod
    async def get_year_show_rating(cls, year: int, show_type: str = None):
        # Use the match stage to filter out documents that satisfy the passed in query operation
        # Include a type query in the match stage if a type is specified; else group by type in group stage
        match_stage = (
            {"$match": {"year": {"$eq": year}}}
            if not show_type
            else {"$match": {"year": {"$eq": year}, "type": show_type}}
        )
        # Group the matched documents by type if no specific type given, else return the average rating of this type
        group_stage = {
            "$group": {
                "_id": "$type" if not show_type else None,
                "averageRating": {"$avg": "$rating"},
            }
        }

        pipeline = [match_stage, group_stage]
        return await cls.driver.aggregate(pipeline).to_list(length=None)

    @classmethod
    async def get_year_statistics(cls, year: int = None):
        match_stage = (
            {"$match": {"year": {"$eq": year}}} if year else None
        )  # Use match stage to filter out documents w/specific year if passed in

        # Group documents by year if no specific year given, else calculate the stats for this group only
        show_group = {
            "$group": {
                "_id": "$year" if not match_stage else None,
                "averageRating": {"$avg": "$runtime"},
                "averageRuntime": {"$avg": "$rating"},
            }
        }
        sort_groups = {"$sort": {"_id": 1}}  # Sort in asc ordr

        pipeline = [show_group, sort_groups]

        # Finally, only include match stage if it's defined
        if match_stage:
            pipeline.insert(0, match_stage)

        return await cls.driver.aggregate(pipeline).to_list(length=None)

    @classmethod
    async def get_director_or_genre_statistics(cls, type: str, value):
        match_stage = {"$match": {type: value}}
        group_stage = {"$group": {"_id": None, "averageRating": {"$avg": "$rating"}}}

        pipeline = [match_stage, group_stage]
        return await cls.driver.aggregate(pipeline).to_list(length=None)
