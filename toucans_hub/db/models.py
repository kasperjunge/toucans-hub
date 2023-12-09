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
    completion_config: dict = Field(default={}, sa_column=Column(JSON))
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )


class CreatePromptFunction(BaseModel):
    name: str
    hash_id: str
    completion_config: dict
