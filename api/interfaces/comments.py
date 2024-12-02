from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import SQLModel
from api.db.models.comments import CommentBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin


class CommentCreate(CommentBase):
    user_id: UUID
    post_id: UUID
    model_config = ConfigDict(extra="forbid")


class CommentRead(CommentBase, IdMixin, TimestampMixin):
    user_id: UUID
    post_id: UUID



class CommentUpdate(SQLModel):
    user_id: UUID
    post_id: UUID
    like_count: Optional[int] = None
    comment: Optional[str] = None

    model_config = ConfigDict(extra="forbid")
