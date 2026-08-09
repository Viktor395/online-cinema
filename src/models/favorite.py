from sqlalchemy import Column, Integer, ForeignKey, Table
from src.core.database import Base


user_favorites = Table(
    "user_favorites",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "movie_id",
        Integer,
        ForeignKey("movies.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
