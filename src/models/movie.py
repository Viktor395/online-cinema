import uuid
from sqlalchemy import Column, Integer, String, Float, DECIMAL, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.core.database import Base

# Таблиці асоціацій для зв'язків багато-до-багатьох
movie_genres = Table(
    "movie_genres",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("genre_id", Integer, ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
)

movie_directors = Table(
    "movie_directors",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("director_id", Integer, ForeignKey("directors.id", ondelete="CASCADE"), primary_key=True),
)

movie_stars = Table(
    "movie_stars",
    Base.metadata,
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
    Column("star_id", Integer, ForeignKey("stars.id", ondelete="CASCADE"), primary_key=True),
)


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)

    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")


class Director(Base):
    __tablename__ = "directors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)

    movies = relationship("Movie", secondary=movie_directors, back_populates="directors")


class Star(Base):
    __tablename__ = "stars"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)

    movies = relationship("Movie", secondary=movie_stars, back_populates="stars")


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)  # наприклад, "PG-13", "R"

    movies = relationship("Movie", back_populates="certification")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(String, unique=True, index=True, nullable=False, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    time = Column(Integer, nullable=False)  # тривалість у хвилинах
    imdb = Column(Float, nullable=False)
    votes = Column(Integer, nullable=False)
    meta_score = Column(Float, nullable=True)
    gross = Column(Float, nullable=True)
    description = Column(Text, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    
    certification_id = Column(Integer, ForeignKey("certifications.id"), nullable=False)
    
    # Зв'язки
    certification = relationship("Certification", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
    directors = relationship("Director", secondary=movie_directors, back_populates="movies")
    stars = relationship("Star", secondary=movie_stars, back_populates="movies")