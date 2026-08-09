# 🎬 Online Cinema API (Backend)

Backend application for an online cinema platform built with **FastAPI**, **PostgreSQL**, and **SQLAlchemy**. It features secure user authentication, catalog management, favorites, cart/orders, and is deployed on a cloud environment.

---

## 🛠 Tech Stack
* **Python**
* **FastAPI** (Asynchronous web framework)
* **SQLAlchemy** (ORM)
* **Alembic** (Database migrations)
* **PostgreSQL** (Relational database)
* **Poetry** (Dependency management)
* **Uvicorn** (ASGI server)
* **AWS EC2** (Cloud hosting)

---

## 🔌 API Endpoints & Features

The API is structured into several main modules:
* **Auth:** User registration, login, and token refresh (`/auth/...`)
* **Movies:** Full CRUD operations for managing movies in the catalog (`/movies/...`)
* **Favorites:** Managing user's favorite movies list (`/favorites/...`)
* **Cart & Orders:** Shopping cart functionality and order creation (`/shop/...`)

---

## 🚀 Quick Start (Local Setup)

You can run this project either directly with Poetry or using Docker.

### Option A: Using Poetry (Recommended for development)
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Viktor395/online-cinema.git](https://github.com/Viktor395/online-cinema.git)
   cd online-cinema

2. **Install dependencies::**
   poetry install

3. **Run migrations & server:::**
   poetry run alembic upgrade head
   poetry run uvicorn src.main:app --reload

### Option B: Using Docker (Recommended for production/deployment)

1. **Build and run the containers:::**
   docker-compose up --build

2. **The application will be automatically configured, and the database will be set up via the service defined in docker-compose.yml.::**

### 📚 API Documentation

Once the server is running, you can explore the interactive API documentation:

Swagger UI: http://3.72.233.254:8000/docs

ReDoc: http://3.72.233.254:8000/redoc

### ☁️ Deployment (AWS EC2)
The project is hosted on AWS EC2. To keep the server running in the background continuously, tmux is used:

### Connect to the server
ssh -i "cinema-key.pem" ubuntu@3.72.233.254

### Start inside a tmux session
tmux new -s cinema
cd online-cinema
poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000

(To detach from the session while keeping it running, press Ctrl + B, then D)
