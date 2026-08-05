from src.core.database import SessionLocal, engine, Base
from src.models.movie import Genre, Certification
# Імпортуємо всі інші моделі, щоб вони зареєструвалися в Base
from src.models.user import UserGroup

def seed_data():
    # Створюємо таблиці напряму через engine, який використовує settings.DATABASE_URL
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Додаємо жанри
        genres = ["Action", "Drama", "Sci-Fi", "Comedy"]
        for g_name in genres:
            existing = db.query(Genre).filter(Genre.name == g_name).first()
            if not existing:
                db.add(Genre(name=g_name))

        # Додаємо вікові сертифікації
        certs = ["PG-13", "R", "PG", "G"]
        for c_name in certs:
            existing = db.query(Certification).filter(Certification.name == c_name).first()
            if not existing:
                db.add(Certification(name=c_name))

        db.commit()
        print("✅ База успішно заповнена тестовими даними!")
    except Exception as e:
        print(f"❌ Помилка при заповненні бази: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()