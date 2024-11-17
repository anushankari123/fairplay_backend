from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import SQLModel
from api.db.models.post import PostBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin


class PostCreate(PostBase):
    user_id: UUID  
    model_config = ConfigDict(extra="forbid")


class PostRead(PostBase, IdMixin, TimestampMixin):
    user_id: UUID


class PostUpdate(SQLModel):
    description: Optional[str] = None
    hashtag: Optional[str] = None
    photo: Optional[str] = None

    model_config = ConfigDict(extra="forbid")
