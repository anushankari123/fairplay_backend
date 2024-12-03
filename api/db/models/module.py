from typing import TYPE_CHECKING
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from .base import IdMixin, TimestampMixin, SoftDeleteMixin, BaseModel

if TYPE_CHECKING:
    from .lesson import Lesson
    from .user import User


class ModuleBase(SQLModel):
    name: str = Field(..., description="Name of the module", nullable=False)
    image_url: str = Field(None, description="URL of the module image", nullable=True)
    quiz_score: int = Field(description="Quiz score of the module", default=0)
    modules_completed: int = Field(description="Number of modules completed", default=0)
    modules_in_progress: int = Field(description="Number of modules in progress", default=0)


class Module(BaseModel, ModuleBase, IdMixin, TimestampMixin, SoftDeleteMixin, table=True):
    __tablename__ = "modules"

    user_id: UUID = Field(..., foreign_key="users.id", description="ID of the user associated with the module")
    user: "User" = Relationship(back_populates="modules")
    lessons: list["Lesson"] = Relationship(
        back_populates="module", sa_relationship_kwargs={"cascade": "all, delete"}
    )

    def __repr__(self):
        return f"<Module (id: {self.id}, name: {self.name}, user_id: {self.user_id})>"
