from sqlalchemy import delete, select, func
from shows.models import Show as PydanticShow, UpdateShowModel, BaseShowService
from fastapi_sqlalchemy import db
from models.pgsql import Show


class ShowService(BaseShowService):
    rating_column = func.avg(Show.rating).label("averageRating")
    runtime_column = func.avg(Show.runtime).label("averageRuntime")

    @classmethod
    def get_all_shows():
        rows = db.session.execute(select(Show))
        rows = [row["Show"] for row in rows]
        return rows

    @classmethod
    def create_show(show: PydanticShow):
        db.session.add(show)

    @classmethod
    def delete_show(cls, show_id: str):
        stmt = delete(Show).where(Show.show_id == show_id)

        db.session.execute(stmt)
        db.session.commit()

    @classmethod
    def update_show(cls, show_id: str, show: UpdateShowModel):
        pass

    ## Aggregation Queries

    @classmethod
    def get_year_show_rating(cls, year: int, show_type: str = None):
        type_condition = Show.type == show_type if show_type else Show.type.is_not(None)
        stmt = select(cls.rating_column).where(Show.year == year).where(type_condition)

        row = db.session.execute(stmt).first()
        return row

    @classmethod
    def get_year_statistics(cls, year: int = None):
        cols = [
            Show.year,
            cls.runtime_column,
            cls.rating_column,
        ]

        stmt = select(cols).where(Show.year == year)

        if not year:
            stmt = select(cols).group_by(Show.year)

        rows = db.session.execute(stmt).all()
        return rows

    @classmethod
    def get_director_or_genre_statistics(cls, type: str, value):
        stmt = f"""
          SELECT avg(rating) AS rating, avg(runtime) AS runtime
          FROM shows
          WHERE {type} @> ARRAY[{value}]::varchar[]
        """

        row = db.session.execute(stmt).first()
        return row
