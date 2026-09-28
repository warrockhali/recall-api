import os
from collections.abc import Iterator
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session


def get_database_url() -> str:
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL must be set before using the database")
    if not url.startswith("postgresql+psycopg://"):
        raise RuntimeError("DATABASE_URL must use the postgresql+psycopg driver")
    return url


@lru_cache
def get_engine() -> Engine:
    return create_engine(
        get_database_url(),
        connect_args={"options": "-c timezone=UTC"},
        pool_pre_ping=True,
    )


def get_session() -> Iterator[Session]:
    with Session(get_engine()) as session:
        yield session
