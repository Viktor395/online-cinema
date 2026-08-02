from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate
from src.core.security import get_password_hash


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate, group_id: int = 1):
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=hashed_password,
        is_active=True,
        group_id=group_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
