from pydantic import BaseModel
from typing import List
from src.schemas.movie import MovieResponse


class FavoriteAdd(BaseModel):
    movie_id: int


class FavoriteResponse(BaseModel):
    favorites: List[MovieResponse]

    class Config:
        from_attributes = True
