from typing import Optional
from uuid import UUID
from pydantic import ConfigDict
from sqlmodel import SQLModel
from api.db.models.lesson import LessonQuizBase
from api.db.models import IdMixin, TimestampMixin, SoftDeleteMixin

class LessonQuizCreate(LessonQuizBase):
    user_id: UUID
    model_config = ConfigDict(extra="forbid")

class LessonQuizRead(LessonQuizBase, IdMixin, TimestampMixin):
    user_id: UUID

class LessonQuizUpdate(SQLModel):
    lesson_name: Optional[str] = None
    l_quizscore: Optional[int] = None

    model_config = ConfigDict(extra="forbid")