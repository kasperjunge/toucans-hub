import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

db_url = os.environ["DATABASE_URL"]
engine = create_engine(db_url)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session
