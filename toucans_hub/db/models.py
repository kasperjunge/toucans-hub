from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import JSON, Field, SQLModel

# ---------------------------------------------------------------------------- #
#                                Prompt Function                               #
# ---------------------------------------------------------------------------- #


class PromptFunction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    hash_id: str = Field(index=True)
    chat_api_config: dict = Field(default={}, sa_column=Column(JSON))
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )


class CreatePromptFunction(BaseModel):
    name: str
    hash_id: str
    chat_api_config: dict


# ---------------------------------------------------------------------------- #
#                                     Users                                    #
# ---------------------------------------------------------------------------- #

from fastapi_users import models
from fastapi_users.db import SQLModelBaseUser
from sqlmodel import Field, SQLModel


class User(SQLModelBaseUser, table=True):
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)


class UserCreate(models.CreateUpdateDictModel):
    first_name: str
    last_name: str
    email: str
    password: str


class UserUpdate(models.CreateUpdateDictModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserDB(User, models.BaseUserDB):
    pass
