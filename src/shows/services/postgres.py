from sqlalchemy import delete, select, func, update
from shows.models import Shows as Show, UpdateShowModel, BaseShowService
from fastapi_sqlalchemy import db


class ShowService(BaseShowService):
    rating_column = func.avg(Show.rating).label("averageRating")
    runtime_column = func.avg(Show.runtime).label("averageRuntime")

    @classmethod
    async def get_all_shows(cls):
        rows = db.session.execute(select(Show))
        rows = [row["Shows"] for row in rows]
        return rows

    @classmethod
    async def create_show(cls, show: Show):
        db.session.add(show)
        db.session.commit()

        return show.show_id if show in db.session else None

    @classmethod
    async def delete_show(cls, show_id: str) -> bool:
        stmt = delete(Show).where(Show.show_id == show_id)

        db.session.execute(stmt)
        db.session.commit()

        return not db.session.execute(
            select(Show).where(Show.show_id == show_id)
        ).first()

    @classmethod
    async def update_show(cls, show_id: str, show: UpdateShowModel):
        stmt = update(Show).where(Show.show_id == show_id).values(show)

        db.session.execute(stmt)
        db.session.commit()

    ## Aggregation Queries

    @classmethod
    async def get_year_show_rating(cls, year: int, show_type: str = None):
        type_condition = Show.type == show_type if show_type else Show.type.is_not(None)

        stmt = (
            select(cls.rating_column, Show.type)
            .where(Show.year == year)
            .where(type_condition)
            .group_by(Show.type)
        )

        row = db.session.execute(stmt).all()
        return row

    @classmethod
    async def get_year_statistics(cls, year: int = None):
        cols = [
            Show.year,
            cls.runtime_column,
            cls.rating_column,
        ]

        condition = Show.year == year if year else Show.year != None
        stmt = select(cols).where(condition).group_by(Show.year)

        rows = db.session.execute(stmt).all()
        return rows

    @classmethod
    async def get_director_or_genre_statistics(cls, type: str, value):
        stmt = f"""
          SELECT avg(rating) AS rating, avg(runtime) AS runtime
          FROM shows
          WHERE {type} @> ARRAY['{value}']::varchar[]
        """

        row = db.session.execute(stmt).first()
        return row
