from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User

class LessonQuizBase(SQLModel):
    lesson_name: str = Field(..., description="Name of the lesson")
    l_quizscore: int = Field(default=0, description="Quiz score for the lesson")

class LessonQuiz(BaseModel, LessonQuizBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "lesson_quizzes"

    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user")
    
    user: "User" = Relationship(back_populates="lesson_quizzes")

    def __repr__(self):
        return f"<LessonQuiz (id: {self.id}, lesson_name: {self.lesson_name}, user_id: {self.user_id})>"