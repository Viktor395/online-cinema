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

    reg_res = client.post("/auth/register", json={
        "email": "orderuser@example.com", 
        "password": "password123", 
        "username": "orderuser"
    })
    
    
    res = client.post("/auth/login", data={
        "username": "orderuser@example.com", 
        "password": "password123"
    })
    
    
    if res.status_code != 200:
        raise Exception(f"Login failed! Status: {res.status_code}, Response: {res.json()}")
    
    data = res.json()
    if "access_token" not in data:
        raise Exception(f"Token not found in response! Response: {data}")
        
    return data["access_token"]

def test_create_order_empty_cart():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.post("/shop/order", headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Cart is empty"

def test_create_order_success():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    
    db = TestingSessionLocal()
    

    cert = Certification(name="PG-13")
    db.add(cert)
    db.commit()
    db.refresh(cert)
    

    movie = Movie(
        title="Avatar", 
        description="3D Movie", 
        price=300.0,
        year=2009,
        time=162,
        imdb=7.9,
        votes=1000000,
        certification_id=cert.id
    )
    db.add(movie)
    db.commit()
    movie_id = movie.id
    db.close()
    

    client.post(f"/shop/cart/add/{movie_id}", headers=headers)
    

    response = client.post("/shop/order", headers=headers)
    assert response.status_code == 201
    assert "order_id" in response.json()
