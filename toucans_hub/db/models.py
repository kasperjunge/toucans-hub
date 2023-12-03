from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlalchemy import JSON, Column
from sqlmodel import JSON, Field, SQLModel


class PromptFunction(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(index=True)
    username: str = Field(index=True, default=None)
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
