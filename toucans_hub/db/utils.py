import os
from typing import Generator

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()


engine = create_engine(os.environ["DB_URL"])
SQLModel.metadata.create_all(engine)
session = Session(engine)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session
