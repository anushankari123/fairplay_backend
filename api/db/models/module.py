from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User

class ModuleQuizBase(SQLModel):
    module_name: str = Field(..., description="Name of the module")
    module_progress: int = Field(default=0, description="Progress of the module")
    module_completed: int = Field(default=0, description="Completion status of the module")
    m_quizscore: int = Field(default=0, description="Quiz score for the module")

class ModuleQuiz(BaseModel, ModuleQuizBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "module_quizzes"

    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user")
    
    user: "User" = Relationship(back_populates="module_quizzes")

    def __repr__(self):
        return f"<ModuleQuiz (id: {self.id}, module_name: {self.module_name}, user_id: {self.user_id})>"