from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings
import os
import json

def get_database_url():
    # Railway provides DATABASE_URL automatically for PostgreSQL
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Fix Railway's postgres:// to postgresql://
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url
    else:
        # Keep SQLite for local development
        os.makedirs(os.path.dirname(settings.DB_PATH), exist_ok=True)
        return f"sqlite:///{settings.DB_PATH}"

# Create engine with the appropriate URL
DATABASE_URL = get_database_url()
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class UserDoc(Base):
    __tablename__ = "user_docs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    path = Column(String)
    meta = Column(Text)  

# Create tables
Base.metadata.create_all(bind=engine)
