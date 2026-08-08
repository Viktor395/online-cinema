from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from src.schemas.user import UserCreate, UserResponse
from src.schemas.token import TokenResponse, RefreshTokenRequest
from src.crud.user import get_user_by_email, create_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Користувач із такою електронною поштою вже зареєстрований."
        )
    
    new_user = create_user(db=db, user_in=user_in)
    return new_user


@router.post("/login", response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = get_user_by_email(db, email=form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильна електронна пошта або пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {"sub": str(user.id), "group_id": user.group_id}
    
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=dict)
def refresh_access_token(body: RefreshTokenRequest):
    payload = verify_refresh_token(body.refresh_token)
    
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недійсний або прострочений refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    group_id = payload.get("group_id")
    
    new_access_token = create_access_token(data={"sub": user_id, "group_id": group_id})
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
