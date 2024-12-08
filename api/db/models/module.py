from datetime import datetime  # Remove timezone import
from uuid import UUID
from typing import TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User
    from .certificate import Certificate

class ModuleQuizBase(SQLModel):
    module_name: str = Field(..., description="Name of the module")
    module_progress: int = Field(default=0, description="Progress of the module")
    module_completed: int = Field(default=0, description="Completion status of the module")
    m_quizscore: int = Field(default=0, description="Quiz score for the module")
    completed_at: datetime | None = Field(
        default=None, 
        description="Timestamp when module was completed"
    )

class ModuleQuiz(BaseModel, ModuleQuizBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "module_quizzes"
    
    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user")
    
    user: "User" = Relationship(back_populates="module_quizzes")
    certificates: "Certificate" = Relationship(back_populates="module_quiz")