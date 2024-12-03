from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .module import Module
    from .user import User


class LessonBase(SQLModel):
    name: str = Field(..., description="Name of the lesson", nullable=False)
    media_url: str = Field(None, description="URL of the media content", nullable=True)
    lesson_quiz: int = Field(description="Score of the lesson quiz", default=0)
    lessons_completed: int = Field(description="Number of lessons completed", default=0)


class Lesson(BaseModel, LessonBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "lessons"

    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user associated with the lesson")
    user: "User" = Relationship(back_populates="lessons")
    module_id: UUID = Field(..., foreign_key="modules.id", description="ID of the module the lesson belongs to")
    module: "Module" = Relationship(back_populates="lessons")

    def __repr__(self):
        return f"<Lesson (id: {self.id}, name: {self.name}, module_id: {self.module_id}, user_id: {self.user_id})>"
