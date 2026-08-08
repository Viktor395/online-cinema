from pydantic import BaseModel
from typing import List
from datetime import datetime
from src.schemas.movie import MovieResponse


class CartResponse(BaseModel):
    id: int
    movies: List[MovieResponse]

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    created_at: datetime
    movies: List[MovieResponse]

    class Config:
        from_attributes = True
