
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE")
POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


if all(
    [
        POSTGRES_HOST,
        POSTGRES_DATABASE,
        POSTGRES_USERNAME,
        POSTGRES_PASSWORD,
    ]
):
    DATABASE_URL = (
        f"postgresql+psycopg://"
        f"{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:5432/{POSTGRES_DATABASE}"
        f"?sslmode=require"
    )

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )
else:
    DATABASE_URL = "sqlite:///./visitas.db"

    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

