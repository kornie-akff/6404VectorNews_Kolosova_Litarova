from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DataBase_URL = "postgresql+psycopg2://postgres:12345@127.0.0.1:5432/vector_news_db"
engine = create_engine(DataBase_URL)
SessionLocal = sessionmaker(bind=engine)

# генератор сессий
def get_db():
    """FastAPI-зависимость: открывает сессию на запрос, закрывает после ответа."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()