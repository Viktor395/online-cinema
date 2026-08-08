from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from src.core.database import Base


order_movies = Table(
    "order_movies",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False, default=0.0)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)


    user = relationship("User", backref="orders")
    movies = relationship("Movie", secondary=order_movies, backref="orders")


cart_movies = Table(
    "cart_movies",
    Base.metadata,
    Column("cart_id", Integer, ForeignKey("carts.id", ondelete="CASCADE"), primary_key=True),
    Column("movie_id", Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True),
)

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)

    user = relationship("User", backref="cart")
    movies = relationship("Movie", secondary=cart_movies, backref="in_carts")
