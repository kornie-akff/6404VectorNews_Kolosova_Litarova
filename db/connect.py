from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine

DataBase_URL = "postgresql+psycopg2://postgres:12345@127.0.0.1:5432/vector_news_db"
engine = create_engine(DataBase_URL)
SessionLocal = sessionmaker(bind=engine)