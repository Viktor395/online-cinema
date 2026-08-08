from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.security import get_current_active_user
from src.models.user import User
from src.models.movie import Movie
from src.models.order import Cart, Order
from src.schemas.order import CartResponse, OrderResponse

router = APIRouter(prefix="/shop", tags=["Cart & Orders"])

# --- Кошик ---
@router.get("/cart", response_model=CartResponse)
def get_cart(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.post("/cart/add/{movie_id}")
def add_to_cart(movie_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    # Викликаємо get_cart всередині або шукаємо напряму
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        cart = Cart(user_id=current_user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie not in cart.movies:
        cart.movies.append(movie)
        db.commit()
    return {"detail": "Movie added to cart"}

# --- Замовлення ---
@router.post("/order", status_code=status.HTTP_201_CREATED)
def create_order(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.movies:
        raise HTTPException(status_code=400, detail="Cart is empty")

    new_order = Order(
        user_id=current_user.id,
        total_price=sum(m.price for m in cart.movies),
        movies=cart.movies
    )
    db.add(new_order)
    
    cart.movies = []
    db.commit()
    db.refresh(new_order)
    return {"detail": "Order created successfully", "order_id": new_order.id}