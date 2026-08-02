from typing import List, Optional
from pydantic import BaseModel, Field, condecimal


class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class DirectorResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class StarResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CertificationResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class MovieResponse(BaseModel):
    id: int
    uuid: str
    title: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    price: float
    certification: CertificationResponse
    genres: List[GenreResponse] = []
    directors: List[DirectorResponse] = []
    stars: List[StarResponse] = []

    class Config:
        from_attributes = True


class MovieCreateUpdate(BaseModel):
    title: str
    year: int
    time: int
    imdb: float
    votes: int
    meta_score: Optional[float] = None
    gross: Optional[float] = None
    description: str
    price: float = Field(..., gt=0)
    certification_id: int
    genre_ids: List[int] = []
    director_ids: List[int] = []
    star_ids: List[int] = []
