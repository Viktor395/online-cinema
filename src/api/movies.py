from typing import List, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.models.movie import Movie, Genre
from src.schemas.movie import MovieResponse, MovieCreateUpdate


router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=List[MovieResponse])
def get_movies(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    genre_id: Optional[int] = None,
    min_rating: Optional[float] = None,
    db: Session = Depends(get_db),
):
    """Отримати список фільмів із пагінацією, пошуком за назвою та фільтрами."""
    query = db.query(Movie)

    # Пошук за назвою
    if search:
        query = query.filter(Movie.title.ilike(f"%{search}%"))

    # Фільтрація за жанром
    if genre_id:
        query = query.filter(Movie.genres.any(Genre.id == genre_id))

    # Фільтрація за мінімальним рейтингом IMDb
    if min_rating:
        query = query.filter(Movie.imdb >= min_rating)

    movies = query.offset(skip).limit(limit).all()
    return movies


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    """Отримати детальну інформацію про конкретний фільм за його ID."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )
    return movie


@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie_in: MovieCreateUpdate, db: Session = Depends(get_db)):
    """Створити новий фільм (доступно для модераторів/адмінів)."""
    new_movie = Movie(
        title=movie_in.title,
        year=movie_in.year,
        time=movie_in.time,
        imdb=movie_in.imdb,
        votes=movie_in.votes,
        meta_score=movie_in.meta_score,
        gross=movie_in.gross,
        description=movie_in.description,
        price=movie_in.price,
        certification_id=movie_in.certification_id,
    )

    # Додаємо зв'язки з жанрами за їх ID
    if movie_in.genre_ids:
        genres = db.query(Genre).filter(Genre.id.in_(movie_in.genre_ids)).all()
        new_movie.genres = genres

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return new_movie


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int, movie_in: MovieCreateUpdate, db: Session = Depends(get_db)
):
    """Оновити інформацію про фільм за його ID."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )

    # Оновлюємо звичайні поля
    movie.title = movie_in.title
    movie.year = movie_in.year
    movie.time = movie_in.time
    movie.imdb = movie_in.imdb
    movie.votes = movie_in.votes
    movie.meta_score = movie_in.meta_score
    movie.gross = movie_in.gross
    movie.description = movie_in.description
    movie.price = movie_in.price
    movie.certification_id = movie_in.certification_id

    # Оновлюємо зв'язки з жанрами (якщо передані)
    if movie_in.genre_ids is not None:
        genres = db.query(Genre).filter(Genre.id.in_(movie_in.genre_ids)).all()
        movie.genres = genres

    db.commit()
    db.refresh(movie)
    return movie


@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    """Видалити фільм за його ID."""
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )

    db.delete(movie)
    db.commit()
    return None
