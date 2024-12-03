from uuid import UUID
from typing import Optional, List
from pydantic import ConfigDict
from datetime import datetime
from sqlmodel import SQLModel

class ForumCreate(SQLModel):
    forum_name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    model_config = ConfigDict(extra="forbid")

class ForumRead(ForumCreate):
    id: UUID

class ForumMemberCreate(SQLModel):
    forum_id: UUID
    user_id: UUID
    model_config = ConfigDict(extra="forbid")

class ForumMemberRead(ForumMemberCreate):
    id: UUID

class ForumMessageCreate(SQLModel):
    forum_id: UUID
    user_id: UUID
    message: str
    image_url: Optional[str] = None
    model_config = ConfigDict(extra="forbid")

class ForumMessageRead(ForumMessageCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime
    user_name: Optional[str] = None
    model_config = ConfigDict(extra="ignore")