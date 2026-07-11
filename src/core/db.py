import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(".env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bank.db")
if not DATABASE_URL or "<" in DATABASE_URL or ">" in DATABASE_URL:
    DATABASE_URL = "sqlite:///./bank.db"

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from src.models.db_models import Base as DbBase

    DbBase.metadata.create_all(bind=engine)
