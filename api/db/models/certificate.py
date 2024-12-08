from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, Optional
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func

from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .user import User
    from .module import ModuleQuiz

class CertificateBase(SQLModel):
    module_name: str = Field(..., description="Name of the module for which the certificate is generated")
    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user who completed the module")
    module_quiz_id: UUID = Field(..., foreign_key="module_quizzes.id", description="ID of the associated module quiz")
    score: int = Field(..., description="Score achieved in the module")
    certificate_url: Optional[str] = Field(default=None, description="URL of the generated certificate")
        
    deleted_at: Optional[datetime] = Field(
        default=None, 
        description="Timestamp of deletion", 
        sa_column=Column(DateTime(timezone=True), nullable=True)
    )
    

class Certificate(BaseModel, CertificateBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__: ClassVar[str] = "certificates"

    user: "User" = Relationship(back_populates="certificates")
    module_quiz: "ModuleQuiz" = Relationship(back_populates="certificates")  # Match "certificates" in ModuleQuiz

    
    def __repr__(self):
        return f"<Certificate (id: {self.id}, module_name: {self.module_name}, user_id: {self.user_id})>"
