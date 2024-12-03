from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import SQLModel
from api.db.models.lesson import LessonBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin


class LessonCreate(SQLModel):
    user_id: UUID
    module_id: UUID
    name: str
    media_url: Optional[str] = None
    model_config = ConfigDict(extra="forbid")


class LessonRead(LessonBase, IdMixin, TimestampMixin):
    user_id: UUID
    module_id: UUID


class LessonUpdate(SQLModel):
    lesson_quiz: Optional[int] = None
    lessons_completed: Optional[int] = None
    model_config = ConfigDict(extra="forbid")
