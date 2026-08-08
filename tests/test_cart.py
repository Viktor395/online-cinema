from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.core.database import Base, get_db
from src.models.movie import Movie, Certification

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = lambda: TestingSessionLocal()
client = TestClient(app)

def get_auth_token():
    client.post("/auth/register", json={
        "email": "cartuser@example.com", 
        "username": "cartuser", 
        "password": "password123"
    })
    res = client.post("/auth/login", data={"username": "cartuser@example.com", "password": "password123"})
    return res.json()["access_token"]

def test_get_cart():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/shop/cart", headers=headers)
    assert response.status_code == 200
    assert "movies" in response.json()

def test_add_to_cart():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    db = TestingSessionLocal()
    
    
    cert = Certification(name="PG-13")
    db.add(cert)
    db.commit()
    db.refresh(cert)
    
    
    movie = Movie(
        title="Matrix",
        description="Action",
        price=200.0,
        year=1999,
        time=120,
        imdb=8.7,
        votes=1000,
        certification_id=cert.id
    )
    db.add(movie)
    db.commit()
    movie_id = movie.id
    db.close()
    

    response = client.post(f"/shop/cart/add/{movie_id}", headers=headers)
    

    assert response.status_code == 200, response.json()
    assert response.json()["detail"] == "Movie added to cart"
