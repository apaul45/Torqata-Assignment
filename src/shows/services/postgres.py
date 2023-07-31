from sqlmodel import delete, select, func, update, Session
from shows.models import Shows as Show, UpdateShowModel, BaseShowService
from main import pg_engine


# Note that functions here are declared async to make them compatible with routes
# In python, coroutine = function that can stop and wait. Similar to js promises
# Declaring as async marks them as coroutines that the (async) routes can then await


class ShowService(BaseShowService):
    session = Session(pg_engine)  # Session represents a "holding" zone for transac
    rating_column = func.avg(Show.rating).label("averageRating")
    runtime_column = func.avg(Show.runtime).label("averageRuntime")

    @classmethod
    async def get_all_shows(cls):
        rows = cls.session.execute(select(Show))
        rows = [row["Shows"] for row in rows]
        return rows

    @classmethod
    async def create_show(cls, show: Show):
        try:
            cls.session.add(show)
            cls.session.commit()

            return show.show_id if show in cls.session else None
        except:
            # Rollback if errors out to prevent future requests failing
            # Rollback is meant to expunge/expire transactions in session
            cls.session.rollback()
            return

    @classmethod
    async def delete_show(cls, show_id: str) -> bool:
        stmt = delete(Show).where(Show.show_id == show_id)

        cls.session.execute(stmt)
        cls.session.commit()

        return not cls.session.execute(
            select(Show).where(Show.show_id == show_id)
        ).first()

    @classmethod
    async def update_show(cls, show_id: str, show: UpdateShowModel):
        try:
            stmt = update(Show).where(Show.show_id == show_id).values(show)

            cls.session.execute(stmt)
            cls.session.commit()
            return show_id
        except:
            cls.session.rollback()
            return

    ## Aggregation Queries
    # Unit of work pattern: pending transactions get flushed from session right before a query
    @classmethod
    async def get_year_show_rating(cls, year: int, show_type: str = None):
        type_condition = Show.type == show_type if show_type else Show.type.is_not(None)

        stmt = (
            select(cls.rating_column, Show.type)
            .where(Show.year == year)
            .where(type_condition)
            .group_by(Show.type)
        )

        row = cls.session.execute(stmt).all()
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

        rows = cls.session.execute(stmt).all()
        return rows

    @classmethod
    async def get_director_or_genre_statistics(cls, type: str, value):
        stmt = f"""
          SELECT avg(rating) AS rating, avg(runtime) AS runtime
          FROM shows
          WHERE {type} @> ARRAY['{value}']::varchar[]
        """

        row = cls.session.execute(stmt).first()
        return row
