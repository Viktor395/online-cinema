from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.movies import router as movies_router
from src.core.database import SessionLocal, Base, engine
from src.models.user import UserGroup, UserGroupEnum
from src.api.favorites import router as favorites_router
from src.api.cart_orders import router as cart_orders_router


app = FastAPI(title="Online Cinema API")

def init_user_groups():
    db = SessionLocal()
    try:
        roles = [UserGroupEnum.USER.value, UserGroupEnum.MODERATOR.value, UserGroupEnum.ADMIN.value]
        for role_name in roles:
            existing = db.query(UserGroup).filter(UserGroup.name == role_name).first()
            if not existing:
                db.add(UserGroup(name=role_name))
        db.commit()
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_user_groups()

app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(favorites_router)
app.include_router(cart_orders_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Online Cinema API!"}
