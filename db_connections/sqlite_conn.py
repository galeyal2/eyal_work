from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session

connection_string = 'sqlite:///./orca.db'
engine = create_engine(connection_string, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SqliteBase = declarative_base()


@contextmanager
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()


def get_db_for_repo() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_query(query:str):
    with get_db() as db:
        db.execute(
            text(query)
        )