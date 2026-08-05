from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.core.database import get_db
from src.models.user import User
from src.models.movie import Movie
from src.schemas.movie import MovieResponse


router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("/", response_model=List[MovieResponse])
def get_favorites(
    current_user: User = Depends(),
    db: Session = Depends(get_db)
):
    return current_user.favorites


@router.post("/{movie_id}", status_code=status.HTTP_201_CREATED)
def add_to_favorites(
    movie_id: int,
    current_user: User = Depends(),
    db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    if movie in current_user.favorites:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Movie already in favorites")

    current_user.favorites.append(movie)
    db.commit()
    return {"detail": "Movie added to favorites"}


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_favorites(
    movie_id: int,
    current_user: User = Depends(),
    db: Session = Depends(get_db)
):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")

    if movie not in current_user.favorites:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Movie not in favorites")

    current_user.favorites.remove(movie)
    db.commit()
    return None
